---
title: HTTP Is Just Text
date: 2021-02-24
author: Danny Hermes (dhermes@bossylobster.com)
tags: HTTP, Protocol
slug: http-is-just-text
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2021-02-24-http-is-just-text.md
---

This is a tiny little note that can help with debugging in some situations.
We'll use netcat (`nc`) to view the **raw** data sent to and returned from
an HTTP server[ref]Note that HTTP/2 is a binary protocol so this only applies
to HTTP/1.1.[/ref].

### Capture a Request

We'll run a dummy listener via `nc` and directly inspect the body of an
HTTP request. To run the listener on port `6426` via `nc -l` (`-l` for listen)
and in another terminal, use `curl` to make a simple HTTP request

```text
$ curl --max-time 1 http://localhost:6426
curl: (28) Operation timed out after 1005 milliseconds with 0 bytes received
```

In our other shell, we should see something like:

```text
$ nc -l 6426
GET / HTTP/1.1
Host: localhost:6426
User-Agent: curl/7.64.1
Accept: */*

$
```

Let's write this to a file so we can keep it around later

```text
$ nc -l 6426 > request.bin
$ hexdump -C request.bin
00000000  47 45 54 20 2f 20 48 54  54 50 2f 31 2e 31 0d 0a  |GET / HTTP/1.1..|
00000010  48 6f 73 74 3a 20 6c 6f  63 61 6c 68 6f 73 74 3a  |Host: localhost:|
00000020  36 34 32 36 0d 0a 55 73  65 72 2d 41 67 65 6e 74  |6426..User-Agent|
00000030  3a 20 63 75 72 6c 2f 37  2e 36 34 2e 31 0d 0a 41  |: curl/7.64.1..A|
00000040  63 63 65 70 74 3a 20 2a  2f 2a 0d 0a 0d 0a        |ccept: */*....|
0000004e
```

In particular note that the newline characters are `0d 0a`, i.e. `\r\n`:

```text
$ python
>>> b'\x0d\x0a'
b'\r\n'
```

### Capture a Response

We'll use an Express server on port `6426` to capture an HTTP response:

```js
const express = require("express");

function main(port) {
  const app = express();

  app.get("/", (_req, res) => {
    res.send("Hello World!\n");
  });

  app.listen(port, () => {
    console.log(`Listening on http://localhost:${port}`);
  });
}

if (require.main === module) {
  main(6426);
}
```

Running this via `node index.js`, we can see what a "regular" `curl` command
returns

```text
$ curl http://localhost:6426
Hello World!
```

In order to see the **raw** TCP response instead of the parsed HTTP response,
we can again use netcat:

```text
$ cat request.bin | nc localhost 6426
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 13
ETag: W/"d-oLZZOWcLwsAQ9NXWoLPk5FkPuSs"
Date: Thu, 25 Feb 2021 04:47:12 GMT
Connection: keep-alive
Keep-Alive: timeout=5

Hello World!
```

As with the request, we see familiar elements of an HTTP response **other**
than the body. For example the first line has the status code and the next
seven lines contain the headers.
