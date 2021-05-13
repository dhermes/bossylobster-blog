---
title: Fixing the Custom CA Problem in Node.js
description: Monkey Patching an Unintuitive API
date: 2021-05-12
author: Danny Hermes (dhermes@bossylobster.com)
tags: Node.js, TLS, Monkey Patch, CA, Certificate Authority
slug: node-ca-append
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/heavy-duty-patch.png
github_slug: content/2021-05-12-node-ca-append.md
---

> **TL;DR**: Using the `ca` field to specify custom CAs (certificate
> authorities) in Node.js is a [footgun][1]. It replaces (rather than appends
> to) the root trust store which can lead to unintended consequences. I've
> seen this behavior cause outages in production when a third party server does
> a routine certificate rotation.
>
> By using the `ca-append` [package][2], the built-in handling in
> Node.js will be monkey patched so that the `ca` field is not supported.
> Instead we replace it with two fields `caAppend` and `caReplace`.

Below we'll run a TLS server using a custom CA certificate. We'll
compare the difference in behavior between `curl` and Node.js when making
TLS requests to this server and to `google.com` with the same configuration.
Finally, after seeing how Node.js differs from `curl` in this regard, we'll
show how to use the `ca-append` [package][2] to fix the issues with the
`ca` TLS option in Node.js.

See [The Node.js CA Footgun][1] for more details on a real world situation
that showcases a problematic situation caused by the behavior of the `ca`
TLS option.

- [Server](#server)
- [Clients](#clients)
- [Append vs. Replace](#append-vs-replace)
- [Patching Node.js](#patching-node-js)

### Server {#server}

We can [define][3] a hello world TLS / HTTPS server with a
[private key][4] / X.509 [certificate][5] pair for `localhost`:

```typescript
const options = {
  key: fs.readFileSync(`${__dirname}/localhost-key.pem`),
  cert: fs.readFileSync(`${__dirname}/localhost-cert.pem`),
};
https
  .createServer(options, (_req, res) => {
    res.writeHead(200);
    res.end('hello world\n');
  })
  .listen(port);
```

Running this server on port 9072, we'll attempt to securely connect
to it in a number of different ways:

```text
$ npx ts-node server.ts 9072
Running TLS server on localhost:9072
```

### Clients {#clients}

#### `curl` Command Line Client

By default, clients don't trust an X.509 certificate signed by a custom CA:

```text
$ curl https://localhost:9072
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.haxx.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
```

so we need to supply a custom CA [certificate][6]:

```text
$ curl --cacert ./root-ca-cert.pem https://localhost:9072
hello world
```

#### Node.js Client {#node-with-ca}

Similarly when using Node.js, the default client options can't verify the
server. However, when specifying `ca` to point at the custom root CA, the
connection succeeds. Running a `client.ts` [script][7] we see:

```text
$ npx ts-node client.ts https://localhost:9072
Using URL="https://localhost:9072";
Failure when `ca` not included:
  error code:    UNABLE_TO_VERIFY_LEAF_SIGNATURE
  error message: unable to verify the first certificate
Success when `ca` included:
  response.status: 200
```

These two requests are made with slightly different configurations:

```typescript
const withoutCA: axios.AxiosRequestConfig = {
  httpsAgent: new https.Agent({
    // ...
  }),
  // ...
};

const withCA: axios.AxiosRequestConfig = {
  httpsAgent: new https.Agent({
    ca: [customRootCA],
    // ...
  }),
  // ...
};
```

### Append vs. Replace {#append-vs-replace}

#### `curl` Command Line Client

When reaching public servers like `google.com`, `curl` can utilize the
root trust store by default:

```text
$ curl \
>   --write-out "Status Code: %{http_code}\n" --output /dev/null --silent \
>   https://www.google.com/
Status Code: 200
```

and supplying `--cacert` doesn't impede this connection:

```text
$ curl \
>   --write-out "Status Code: %{http_code}\n" --output /dev/null --silent \
>   --cacert ./root-ca-cert.pem \
>   https://www.google.com/
Status Code: 200
```

In other words, `--cacert` **appends** to the root trust store (as opposed to
**replacing** it).

#### Node.js Client

On the other hand, using our Node.js client to reach Google's servers, we
see that the presence of `ca` keeps us from trusting a CA in our root trust
store:

```text
$ npx ts-node client.ts https://www.google.com/
Using URL="https://www.google.com/";
Success when `ca` not included:
  response.status: 200
Failure when `ca` included:
  error code:    UNABLE_TO_GET_ISSUER_CERT_LOCALLY
  error message: unable to get local issuer certificate
```

This should be somewhat jarring; we expect the CA for `google.com` to
**always** be trustworthy.

### Patching Node.js {#patching-node-js}

In order to fix this problem with Node.js, i.e. to provide a way to
**append to** rather than **replace** the root trust store, I have
[written][8] the `ca-append` package. To use the package, import it and
activate the monkey patch:

```typescript
import * as caAppend from 'ca-append';
caAppend.monkeyPatch();
```

and it will monkey patch the core `tls.createSecureContext()` function.

Once patched, the `ca` option will be rejected and replaced with choices that
are more descriptive: `caAppend` and `caReplace`. Let's see the `caAppend`
option in use as well as **rejection** of the `ca` option. First we'll
re-attempt communicating with our server running on `localhost` and
observe the same behavior we saw above in [Node.js Client](#node-with-ca):

```text
$ npx ts-node clientPatched.ts https://localhost:9072
Using URL="https://localhost:9072";
Failure when `ca` / `caAppend` not included:
  error code:    UNABLE_TO_VERIFY_LEAF_SIGNATURE
  error message: unable to verify the first certificate
Failure when `ca` included:
  error code:    undefined
  error message: tls.createSecureContext(): `ca` option has been deprecated
Success when `caAppend` included:
  response.status: 200
```

The connection to Google servers now works in both cases as well:

```text
$ npx ts-node clientPatched.ts https://www.google.com/
Using URL="https://www.google.com/";
Success when `ca` / `caAppend` not included:
  response.status: 200
Failure when `ca` included:
  error code:    undefined
  error message: tls.createSecureContext(): `ca` option has been deprecated
Success when `caAppend` included:
  response.status: 200
```

This all comes from [using][9] `caAppend` in `clientPatched.ts`:

```typescript
const optionsWithCAAppend = makeOptions({ caAppend: [customRootCA] });
```

versus using `ca` in `client.ts`:

```typescript
const optionsWith = makeOptions({ ca: [customRootCA] });
```

### Post Script: Warning {#post-script}

The Node.js module system returns a singleton for every import, so once
`ca-append` monkey patches the `tls` package, every other import of
`tls` will see the effects. This will likely not be directly visible in
application code; `tls` is more likely to be imported transitively in an
application by packages that provide HTTP / HTTPS clients.

[1]: /2021/05/node-ca-footgun.html
[2]: https://www.npmjs.com/package/ca-append
[3]: /code/node-ca/server.ts
[4]: /code/node-ca/localhost-key.pem
[5]: /code/node-ca/localhost-cert.pem
[6]: /code/node-ca/root-ca-cert.pem
[7]: /code/node-ca/client.ts
[8]: https://github.com/dhermes/ca-append-js
[9]: /code/node-ca/clientPatched.ts
