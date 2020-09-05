---
title: Reading Istio Secrets
description: Using gRPC and SDS to read a workload's private key
date: 2020-09-04
author: Danny Hermes (dhermes@bossylobster.com)
tags: gRPC, Envoy, Istio, SDS, Go, Golang
slug: istio-workload-secrets
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/istio-logo.png
github_slug: content/2020-09-04-istio-workload-secrets.md
---

Adopting a service mesh like Istio is a **huge** undertaking. (Let's set aside
for this discussion whether it's a [good idea][1] to undertake.) A fairly
common issue when getting a mesh up and running is misconfiguration. When
trying to debug and determine where and how things are misconfigured, the
network is usually not an ally.

![Istio](/images/istio-whitelogo-bluebackground-framed.svg)

### The Plan

A common option when "the network is broken" and we're flying blind is to use
a packet sniffer to debug. On a development machine, that'd probably be
[Wireshark][2]. In Kubernetes, `ksniff` is a popular [tool][3] to capture
packets and send them back to a development machine for inspection. However,
when the connections are encrypted with TLS, captured packets are not so
useful. For "modern" TLS connections, Wireshark requires a client random data
for the session (see `SSLKEYLOGFILE`) and the private key that encrypted the
traffic.

In this post, we'll be grabbing the private key from a Kubernetes container
in an Istio service mesh to aid in a debugging process. This is something a
cluster administrator would be doing, not an every day thing and not something
a "service owner" would be expected to do. I am writing this up because I
was frustrated by lack of materials found when searching how to do this.

### Envoy and Existing Support

Kubernetes containers in the Istio service mesh run a sidecar container with
Envoy proxy running. In most cases, this sidecar runs in `iptables` mode.
In this mode, it tells the Linux kernel (via `iptables`) that Envoy will be
handling all[ref]Not **all**, really **most**[/ref] network traffic in the
pod. In other words, Envoy has **full control** of the network for any workload
it is running next to as a sidecar.

The Envoy [traffic tap][4] feature exists for capturing potentially encrypted
packets in a `.pcap` file[ref]The file format used by Wireshark and
`tcpdump`[/ref]. See the
[Solving Microservice Mysteries With Envoy's Tap Filter][5] for a pretty great
explainer on using traffic tap.

It would be perfectly fine to just stop here and say "use traffic tap".
However, I kept pulling the thread. At the end of the day, traffic tap is
white box / clear box debugging into the **known** behavior of Envoy. However,
one of the primary use cases of packet capture is to do black box debugging
of unknown or unexpected behavior. So in some sense they are at odds.

### Istio and mTLS

One of the primary wins for a service mesh is enhanced security and zero trust
networking. By requiring workloads to communicate via mutual TLS (mTLS),
the underlying Kubernetes network (and the cloud provider VPC it sits on top
of) will only see TLS packets that have been mutually verified.

Due to the use of mTLS, it's crucial that every workload (i.e. pod) in the
mesh has a unique private key and X.509 public certificate. This pair is used
as proof of identity when negotiating mTLS connections. So getting access to
the key for a given workload is crucial to decrypting the traffic.

### Running the Script

Luckily Envoy has created an incredibly good idea: the [xDS protocol][6].
The `x` stands for "anything here" and the `DS` for "discovery service". The
whole idea underpinning xDS is that different types of configuration are
relevant (and changing over time) to an Envoy proxy server. The ability
to discover and listen for configuration updates over a range of topics is
incredibly useful for a running server. This protocol is making [traction][7]
directly into gRPC as a way to have all of the benefits of dynamic
configuration without the need for a proxy sidecar.

The xDS protocol includes SDS &mdash; secrets discovery service &mdash; which
we'll utilize to grab our private key. The `istio-sds.go` [script][100]
facilitates this in several steps.

#### Determine Envoy Node ID

Invoke `GET /server_info` in the Envoy [admin API][8] to determine the
`command_line_options.service_node` (i.e. the workload or pod identifier
according to Envoy).

```
root@some-istio-workload-748cc777bc-mvqcf:/# curl http://localhost:15000/server_info
{
 "version": "73f240a29bece92a8882a36893ccce07b4a54664/1.13.1-dev/Clean/RELEASE/BoringSSL",
 "state": "LIVE",
 "hot_restart_version": "11.104",
 "command_line_options": {
  ...
  "service_node": "router~10.101.236.171~some-istio-workload-748cc777bc-mvqcf.testing~testing.svc.cluster.local",
  "service_zone": "",
  "mode": "Serve",
  ...
 },
 "uptime_current_epoch": "2424451s",
 "uptime_all_epochs": "2424451s"
}
```

#### Connect to Secrets Discovery Service (SDS)

Open a gRPC connection to the `/etc/istio/proxy/SDS` [UDS][9] that is
mounted in the `istio-proxy` sidecar container. As the `/SDS` in the socket
name indicates, this is the secrets discovery service.

```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
// ...
conn, err := grpc.Dial(target, grpc.WithInsecure(), grpc.WithBlock())
// ...
c := discoveryv2.NewSecretDiscoveryServiceClient(conn)
```

#### Fetch Secret(s) for Current Envoy Node

Call the `FetchSecrets` RPC [method][10] with the `node.id` [field][11]
set to the `command_line_options.service_node` workload identifier

```go
request := &apiv2.DiscoveryRequest{Node: &corev2.Node{Id: serviceNode}}
response, err := c.FetchSecrets(ctx, request, grpc.Header(&header), grpc.Trailer(&trailer))
```

#### Parse the Response

Ensure the `type_url` in the response indicates a
`envoy.api.v2.auth.Secret` and than parse the protobuf `Any` in the
`resources[0]` field as a secret:

```go
secret := &authv2.Secret{}
err := ptypes.UnmarshalAny(response.Resources[0], secret)
// ...
tc := secret.GetTlsCertificate()
cc := tc.GetCertificateChain()
// ...
ccBytes := cc.GetInlineBytes()
pk := tc.GetPrivateKey()
// ...
pkBytes := pk.GetInlineBytes()
```

#### Putting It All Together

<!-- For posterity

```
$ go version
go version go1.15.1 linux/amd64
$
$ git --git-dir ${GOPATH}/src/github.com/envoyproxy/go-control-plane/.git log -1
commit b304c9d56d80fc38b0685bbb42bee68e8270337a (HEAD -> master, origin/master, origin/HEAD)
Author: go-control-plane(CircleCI) <go-control-plane@users.noreply.github.com>
Date:   Fri Sep 4 02:38:16 2020 +0000

    Mirrored from envoyproxy/envoy @ 9d466c71ab217317d3e989b261eb496877348a47

    Signed-off-by: go-control-plane(CircleCI) <go-control-plane@users.noreply.github.com>
```
-->

Running the script on an Istio / Envoy sidecar will (almost certainly)
require building the binary on a different machine since the container
won't have the toolchain installed[ref]If the entire filesystem in the sidecar
is read-only, it's **impossible** to `kubectl cp` a pre-built binary into the
container[/ref]. First build the binary:

```
$ GOARCH=amd64 GOOS=linux go build -o istio-sds-linux-amd64 ./istio-sds.go
```

then copy it into the container

```
$ kubectl cp \
>   --namespace testing \
>   --container istio-proxy \
>   ./istio-sds-linux-amd64 \
>   some-istio-workload-748cc777bc-mvqcf:/usr/local/bin/istio-sds-linux-amd64
```

Finally, run the binary in the `istio-proxy` container to see both the
(public) certificate chain and the private key:

```
$ kubectl exec \
>   --stdin --tty \
>   --namespace testing \
>   --container istio-proxy \
>   some-istio-workload-748cc777bc-mvqcf \
>   -- /usr/local/bin/istio-sds-linux-amd64
19:53:34.710854 istio-sds.go:50:  GET http://localhost:15000/server_info
19:53:34.713220 istio-sds.go:197: Service Node: "router~10.101.236.171~some-istio-workload-748cc777bc-mvqcf.testing~testing.svc.cluster.local"
19:53:34.713247 istio-sds.go:200: Target: "unix:///etc/istio/proxy/SDS"
19:53:34.990037 istio-sds.go:211:
19:53:34.990069 istio-sds.go:212: DiscoveryResponse.VersionInfo: "09-04 19:53:34.715"
19:53:34.990097 istio-sds.go:213: DiscoveryResponse.TypeUrl: "type.googleapis.com/envoy.api.v2.auth.Secret"
19:53:34.990128 istio-sds.go:176: DiscoveryResponse.Resources[0].GetTlsCertificate()
19:53:34.990145 istio-sds.go:177:   GetCertificateChain():
19:53:34.990164 istio-sds.go:179:     -----BEGIN CERTIFICATE-----
19:53:34.990179 istio-sds.go:179:     ...
19:53:34.990421 istio-sds.go:179:     -----END CERTIFICATE-----
19:53:34.990428 istio-sds.go:179:     -----BEGIN CERTIFICATE-----
19:53:34.990435 istio-sds.go:179:     ...
19:53:34.990634 istio-sds.go:179:     -----END CERTIFICATE-----
19:53:34.990647 istio-sds.go:179:
19:53:34.990661 istio-sds.go:181:   GetPrivateKey():
19:53:34.990706 istio-sds.go:183:     -----BEGIN RSA PRIVATE KEY-----
19:53:34.990716 istio-sds.go:183:     ...
19:53:34.991035 istio-sds.go:183:     -----END RSA PRIVATE KEY-----
19:53:34.991049 istio-sds.go:183:
```

[1]: https://twitter.com/rakyll/status/1173663473357574144
[2]: https://www.wireshark.org/
[3]: https://github.com/eldadru/ksniff
[4]: https://www.envoyproxy.io/docs/envoy/latest/operations/traffic_tapping
[5]: https://medium.com/@mtchkll/solving-microservice-mysteries-with-envoys-tap-filter-fd159c36d0af
[6]: https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol
[7]: https://cloud.google.com/blog/products/networking/traffic-director-supports-proxyless-grpc
[8]: https://www.envoyproxy.io/docs/envoy/latest/operations/admin#get--server_info
[9]: https://en.wikipedia.org/wiki/Unix_domain_socket
[10]: https://github.com/envoyproxy/envoy/blob/9d466c71ab217317d3e989b261eb496877348a47/api/envoy/service/discovery/v2/sds.proto#L32
[11]: https://github.com/envoyproxy/envoy/blob/9d466c71ab217317d3e989b261eb496877348a47/api/envoy/api/v2/discovery.proto#L35
[100]: /code/istio-sds.go
[101]: https://github.com/envoyproxy/go-control-plane/tree/b304c9d56d80fc38b0685bbb42bee68e8270337a/envoy/api/v2/core
[102]: https://github.com/envoyproxy/envoy/blob/9d466c71ab217317d3e989b261eb496877348a47/api/envoy/api/v2/auth/secret.proto#L37
[103]: x
[104]: x
[105]: x
[106]: x
[107]: x
