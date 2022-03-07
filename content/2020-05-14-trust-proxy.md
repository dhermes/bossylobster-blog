---
title: Express Trust Proxy
description: Securing Internal Services
date: 2020-05-14
author: Danny Hermes (dhermes@bossylobster.com)
tags: Node.js, Proxy
slug: trust-proxy
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2020-05-14-trust-proxy.md
---

### Why?

Using `app.use('trust proxy', true)` is likely too permissive, this post
explains concretely why.

### Example Applications

Consider two Express applications `index-first.js` that uses
`app.set("trust proxy", true)`

```javascript
const express = require("express");
const app = express();
const port = 3000;

app.set("trust proxy", true);
app.get("/", (req, res) =>
  res.send(
    [
      "req.ip: ",
      JSON.stringify(req.ip),
      "\nreq.xff: ",
      JSON.stringify(req.headers["x-forwarded-for"]),
    ].join("")
  )
);
app.listen(port, () => console.log(`Example app listening on port ${port}!`));
```

and `index-last.js` that uses `app.set("trust proxy", 1)`

```javascript
const express = require("express");
const app = express();
const port = 3001;

app.set("trust proxy", 1);
app.get("/", (req, res) =>
  res.send(
    [
      "req.ip: ",
      JSON.stringify(req.ip),
      "\nreq.xff: ",
      JSON.stringify(req.headers["x-forwarded-for"]),
    ].join("")
  )
);
app.listen(port, () => console.log(`Example app listening on port ${port}!`));
```

### Incoming Requests

We can run both Express applications on ports 3000 and 3001

```
$ node index-first.js
Example app listening on port 3000!
$ node index-last.js
Example app listening on port 3001!
```

#### Plain HTTP

##### With `app.set("trust proxy", true)`

**Observe**: the `req.ip` value will always be the **first** / **leftmost**
value in the `X-Forwarded-For` header (if provided), and falls back to the
IP on the socket (`::1` is the IPv6 loopback / `localhost`) if the header
is absent:

```
$ curl http://localhost:3000
req.ip: "::1"
req.xff: undefined
$ curl --header 'X-Forwarded-For: 127.0.0.2' http://localhost:3000
req.ip: "127.0.0.2"
req.xff: "127.0.0.2"
$ curl --header 'X-Forwarded-For: 127.0.0.3,127.0.0.2' http://localhost:3000
req.ip: "127.0.0.3"
req.xff: "127.0.0.3,127.0.0.2"
$ curl --header 'X-Forwarded-For: 127.0.0.4,127.0.0.3,127.0.0.2' http://localhost:3000
req.ip: "127.0.0.4"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2"
```

This means if a **client** provides an arbitrary / spoofed header they can
place any IP they like in `req.ip`.

##### With `app.set("trust proxy", 1)`

**Observe**: the `req.ip` value will always be the **last** / **rightmost**
value in the `X-Forwarded-For` header (if provided), and falls back to the
IP on the socket (`::1` is the IPv6 loopback / `localhost`) if the header
is absent:

```
$ curl http://localhost:3001
req.ip: "::1"
req.xff: undefined
$ curl --header 'X-Forwarded-For: 127.0.0.2' http://localhost:3001
req.ip: "127.0.0.2"
req.xff: "127.0.0.2"
$ curl --header 'X-Forwarded-For: 127.0.0.3,127.0.0.2' http://localhost:3001
req.ip: "127.0.0.2"
req.xff: "127.0.0.3,127.0.0.2"
$ curl --header 'X-Forwarded-For: 127.0.0.4,127.0.0.3,127.0.0.2' http://localhost:3001
req.ip: "127.0.0.2"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2"
```

#### HTTPS: Behind TLS Proxy

We can use Caddy, NGINX, HAProxy or a similar tool as a TLS reverse proxy and
locally put our services behind this proxy[ref]For the proxy, I used a
[certificate][4] `localhost-cert.pem` and [key][5] `localhost-key.pem` that
are signed by a local [root CA][6].[/ref]. We can use port 8443 to proxy
port 3000 (`index-first.js`) and port 9443 to proxy port 3001
(`index-last.js`).

When calling these TLS servers, we use `curl --haproxy-protocol` to
"simulate" the [PROXY protocol][1] prefix at the beginning of the TCP
data stream.

##### With `app.set("trust proxy", true)`

**Observe**: the TLS reverse proxy modifies the incoming `X-Forwarded-For`
header by **appending** the caller's IP (determined by the PROXY protocol
prefix). If the `X-Forwarded-For` is absent, the caller's IP will be the
only entry in it.

```
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   https://localhost:8443
req.ip: "::1"
req.xff: "::1"
$
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.2' \
>   https://localhost:8443
req.ip: "127.0.0.2"
req.xff: "127.0.0.2, ::1"
$
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.3,127.0.0.2' \
>   https://localhost:8443
req.ip: "127.0.0.3"
req.xff: "127.0.0.3,127.0.0.2, ::1"
$
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.4,127.0.0.3,127.0.0.2' \
>   https://localhost:8443
req.ip: "127.0.0.4"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2, ::1"
$
$ # Drop the PROXY protocol prefix
$ curl \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.4,127.0.0.3,127.0.0.2' \
>   https://localhost:8443
req.ip: "127.0.0.4"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2, ::1"
```

As before since the **first** entry will be used, the PROXY protocol provided
IP will only be used if the client **did not** send an `X-Forwarded-For`
header.

##### With `app.set("trust proxy", 1)`

```
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   https://localhost:9443
req.ip: "::1"
req.xff: "::1"
$
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.2' \
>   https://localhost:9443
req.ip: "::1"
req.xff: "127.0.0.2, ::1"
$
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.3,127.0.0.2' \
>   https://localhost:9443
req.ip: "::1"
req.xff: "127.0.0.3,127.0.0.2, ::1"
$
$ curl \
>   --haproxy-protocol \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.4,127.0.0.3,127.0.0.2' \
>   https://localhost:9443
req.ip: "::1"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2, ::1"
$
$ # Drop the PROXY protocol prefix
$ curl \
>   --cacert ./rootCA-cert.pem \
>   --header 'X-Forwarded-For: 127.0.0.4,127.0.0.3,127.0.0.2' \
>   https://localhost:9443
req.ip: "::1"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2, ::1"
```

##### Simulating an AWS ELB PROXY Protocol

Using `curl --proxy-protocol` didn't provide much value because the
"simulated" client IP was `::1`.

To really drive the point home, we can use the Python script
`haproxy_client.py` to customize the PROXY protocol prefix by prepending
`PROXY TCP4 198.51.100.22 203.0.113.7 35646 80\r\n` before sending the
request over TLS:

```python
import socket
import ssl
import sys


def main():
    port = "8443" if len(sys.argv) < 2 else sys.argv[1]
    port_int = int(port)
    port = port.encode("ascii")  # `bytes`

    context = ssl.create_default_context(cafile="./rootCA-cert.pem")
    haproxy_prefix = b"PROXY TCP4 198.51.100.22 203.0.113.7 35646 80\r\n"
    http_body = b"\r\n".join(
        [
            b"GET / HTTP/1.1",
            b"Host: localhost:" + port,
            b"User-Agent: python-raw-socket",
            b"X-Forwarded-For: 127.0.0.4,127.0.0.3,127.0.0.2",
            b"Accept: */*",
            b"",
            b"",
        ]
    )

    with socket.create_connection(("localhost", port_int)) as sock:
        bytes_sent = sock.send(haproxy_prefix)
        assert bytes_sent == len(haproxy_prefix)
        with context.wrap_socket(sock, server_hostname="localhost") as ssock:
            bytes_sent = ssock.send(http_body)
            assert bytes_sent == len(http_body)
            response_data = ssock.read(1024)
            assert len(response_data) < 1024
            print(response_data.decode("ascii"))


if __name__ == "__main__":
    main()
```

Running it against our two TLS ports we see the difference between the spoofed
"first" IP `127.0.0.4` in the `X-Forwarded-For` header and our desired client
IP (`198.51.100.22`) from the PROXY protocol prefix line

```
$ python haproxy_client.py 8443
HTTP/1.1 200 OK
Content-Length: 76
Content-Type: text/html; charset=utf-8
Date: Mon, 30 Mar 2020 01:25:11 GMT
Etag: W/"4c-o7XjqzEh2LNIL5fg9aGvOinphjw"
X-Powered-By: Express

req.ip: "127.0.0.4"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2, 198.51.100.22"

$
$ python haproxy_client.py 9443
HTTP/1.1 200 OK
Content-Length: 80
Content-Type: text/html; charset=utf-8
Date: Mon, 30 Mar 2020 01:25:06 GMT
Etag: W/"50-7DCPwCaoMhDpTeV3xU491pqi5q4"
X-Powered-By: Express

req.ip: "198.51.100.22"
req.xff: "127.0.0.4,127.0.0.3,127.0.0.2, 198.51.100.22"
```

[1]: https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-proxy-protocol.html
[2]: /code/caddy.8443-proxy-3000.json
[3]: /code/caddy.9443-proxy-3001.json
[4]: /code/localhost-cert.pem
[5]: /code/localhost-key.pem
[6]: /code/rootCA-cert.pem
