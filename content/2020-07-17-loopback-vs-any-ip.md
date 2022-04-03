---
title: Difference Between `localhost` and `0.0.0.0`
date: 2020-07-17
author: Danny Hermes (dhermes@bossylobster.com)
tags: Localhost, Node.js
slug: loopback-vs-any-ip
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2020-07-17-loopback-vs-any-ip.md
---

> **Note**: In a `docker` container, a server can only be available
> **outside of the container / pod** if it is bound to the "any host"
> IP[ref]The "any host" IP is `0.0.0.0` for IPv4 and `::` for IPv6[/ref].
> Binding a server to `localhost` / the loopback IP[ref]The loopback IP is
> `127.0.0.1` for IPv4 and `::1` for IPv6.[/ref] will mean the server is
> only reachable within the container / pod.

Consider the following Express application which binds to the default IP for
port 3000, explicitly binds to `127.0.0.1` for port 4000 and explicitly binds
to `0.0.0.0` for port 5000:

```js
// index.js
const express = require("express");
const app = express();
app.get("/", (req, res) => res.send("Hello World!\n"));
app.listen(3000, () => console.log("Listening on port 3000"));
app.listen(4000, "127.0.0.1", () => console.log("Listening on port 4000"));
app.listen(5000, "0.0.0.0", () => console.log("Listening on port 5000"));
```

We'll install `express` and run this application in a Docker container

```console
docker run \
  --name loopback_unreachable \
  --rm --detach \
  --publish 3001:3000 \
  --publish 4001:4000 \
  --publish 5001:5000 \
  --workdir /var/code \
  --volume $(pwd)/index.js:/var/code/index.js \
  node:12.18.1-alpine3.12 \
  /bin/sh -c 'npm install express@4.17.1 && node /var/code/index.js'
```

From the `--publish` flags we can see the server ports from the container
have been exposed by adding one to each port value. Trying to hit these
ports on the host[ref]To clarify, "on the host" is meant to distinguish from
"inside the container".[/ref], we can see port `4001` &mdash; the
one that is bound explicitly to `127.0.0.1` in the container &mdash; is
unreachable:

```console
$ curl http://localhost:3001
Hello World!
$ curl http://localhost:4001
curl: (52) Empty reply from server
$ curl http://localhost:5001
Hello World!
```

Don't forget to clean up:

```console
docker rm --force loopback_unreachable
```
