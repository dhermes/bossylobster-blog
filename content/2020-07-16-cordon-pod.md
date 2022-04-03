---
title: Isolating (Cordoning) a Misbehaving Pod
date: 2020-07-16
author: Danny Hermes (dhermes@bossylobster.com)
tags: Kubernetes, Pod, Cordon
slug: cordon-pod
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2020-07-16-cordon-pod.md
---

> **TL;DR**: You can remove a misbehaving pod from a service without deleting
> it. Use `kubectl label pod ... cyberdyne-service- ...` to remove a
> label / labels. Once the labels are gone it will be removed from the
> Kubernetes service that routes traffic to pods.

When a Kubernetes **node** is misbehaving, it's common to cordon that
node via

```console
kubectl cordon ip-10-10-9-94.ec2.internal
```

It turns out, it's not as simple to do this for a misbehaving **pod**. In
order to do the same for a pod, we remove the labels used by the Kubernetes
service that routes traffic to pods via a selector and the Kubernetes
deployment that manages creation of pods, scaling, etc.

Per [recommendations][1] from `kubernetes-dev`, determine the pod labels that
keep it in a deployment

```console
$ kubectl get pods --namespace cyberdyne --selector cyberdyne-service=dhermes-echo
NAME                            READY   STATUS    RESTARTS   AGE
dhermes-echo-6c69bf4f49-6zbmx   3/3     Running   0          79m
$
$ kubectl get deployment \
>   --namespace cyberdyne \
>   dhermes-echo \
>   --output go-template='{{ range $k, $v := .spec.selector.matchLabels }}{{ $k }} -> {{ $v }}{{ "\n" }}{{ end }}'
cyberdyne-role -> service-instance
cyberdyne-service -> dhermes-echo
cyberdyne-service-env -> sandbox
```

then remove one (or all) of those labels, this will bring up a new pod
and keep the old one running

```console
$ kubectl label pod \
>   --namespace cyberdyne \
>   dhermes-echo-6c69bf4f49-6zbmx \
>   frozen=dhermes-experiment \
>   cyberdyne-role- \
>   cyberdyne-service- \
>   cyberdyne-service-env-
pod/dhermes-echo-6c69bf4f49-6zbmx labeled
$
$ kubectl get pods --namespace cyberdyne --selector cyberdyne-service=dhermes-echo
NAME                            READY   STATUS    RESTARTS   AGE
dhermes-echo-6c69bf4f49-8tmrf   3/3     Running   0          20s
$
$ kubectl get pods --namespace cyberdyne --selector cyberdyne-deploy=bcxsl9xf
NAME                            READY   STATUS    RESTARTS   AGE
dhermes-echo-6c69bf4f49-6zbmx   3/3     Running   0          86m
dhermes-echo-6c69bf4f49-8tmrf   3/3     Running   0          51s
```

and the service doesn't skip a beat

```console
$ curl https://dhermes-echo.sandbox.k8s.invalid/headers
{"Accept":["*/*"],"Accept-Encoding":["gzip"],"User-Agent":["curl/7.64.1"],"X-Forwarded-For":["10.131.12.77"],"X-Forwarded-Port":["443"],"X-Forwarded-Proto":["https"]}
```

Additionally, the liveness and readiness probes can be removed from any
containers that have them, so the bad behavior can be left alone

```console
$ kubectl edit pod --namespace cyberdyne dhermes-echo-6c69bf4f49-6zbmx
```

> **Tip**: I usually set `KUBE_EDITOR=emacs` or `KUBE_EDITOR='code --wait'` when
> running `kubectl edit`. The default editor it uses likely won't be what you
> want.

Don't forget to clean up the pod when done debugging

```console
$ kubectl delete pod --namespace cyberdyne dhermes-echo-6c69bf4f49-6zbmx
```

[1]: https://groups.google.com/g/kubernetes-dev/c/-sCoM9evaVg
