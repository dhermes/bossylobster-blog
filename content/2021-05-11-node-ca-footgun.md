---
title: The Node.js CA Footgun
description: A Story of an Outage and Unintuitive API
date: 2021-05-11
author: Danny Hermes (dhermes@bossylobster.com)
tags: Node.js, TLS, CA, Certificate Authority
slug: node-ca-footgun
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/door-nowhere.jpg
github_slug: content/2021-05-11-node-ca-footgun.md
---

<div markdown="1" style="text-align: center;">
  ![Door to Nowhere][1]
</div>

This is a story of a brief outage caused by a slightly unintuitive API[ref]Like
a door to nowhere.[/ref] that has some very [sharp corners][7] for the
uninitiated. The outage, though brief, was of the "wake up at 4am" variety so
the lesson was especially salient.

This **is not** a post trying to tear down the Node.js authors or cast blame.
The Node.js runtime and standard library are incredible force multipliers
that help teams ship code quickly. This particular story is about a codebase
misusing the connection options offered by the `tls` package in the Node.js
standard library. This usage was based on an "obvious" interpretation of one
option name and an expectation that another option would behave similarly to
how it works in other technology stacks. These options are very
well documented, but one option could really benefit from being renamed and the
other could benefit from a small change in behavior. However, for a programming
language runtime with such a large userbase it's essentially impossible to
rename options or change behavior in a core package once released.

### Contents

-   [The Good](#the-good)
-   [The Bad](#the-bad)
-   [The Ugly](#the-ugly)
-   [Takeaways](#takeaways)

### The Good {#the-good}

This outage motivated me to try to address the biggest issue in this
outage: the `ca` TLS option wipes away the default root trust store.
I'll be writing up "Fixing the Custom CA Problem in Node.js" soon to showcase
how `ca` is currently broken and to demonstrate how my `ca-append` [package][6]
tries to patch the brokenness.

### The Bad {#the-bad}

Here I want to lay out the sharpest corner: the `ca` TLS option in Node.js
(I mentioned two connection options in this story, but the second one &mdash;
`cert` &mdash; was a less significant contributor to the outage).

When applications securely connect over TLS, they always[ref]Almost always. But
they **should** always verify.[/ref] verify that the server's X.509 certificate
has been signed by a trusted certificate authority (CA). Most language
runtimes &mdash; including Node.js &mdash; have a default root trust store of
well-known CAs.

However, some applications need to connect to private or internal servers that
have X.509 certificates signed by a CA **outside of** the default root trust
store. For example, during local development we may want to run a server over
TLS on `localhost`. Or, some third parties may have a private CA that
they use to sign certificates for internal APIs.

In these situations it's crucial to be able to modify the default root trust
store and Node.js provides a `ca` TLS connection option[ref]
Node.js also supports a `NODE_EXTRA_CA_CERTS` environment variable for the
custom CA use case. However, `NODE_EXTRA_CA_CERTS` is a "catch-all" that
applies to every connection, which can be a problem in multi-tenant
applications.[/ref] for doing just that. The problem with the [`ca` option][2]
is that it completely replaces the existing trust store (rather than appending
to it):

> Optionally override the trusted CA certificates. Default is to trust the
> well-known CAs curated by Mozilla. Mozilla's CAs are completely replaced
> when CAs are explicitly specified using this option.

This means that we can no longer hit public servers over TLS if the `ca` option
is used. For example, we'd expect to be able to communicate with
`https://www.google.com` but unless the CA that signed the Google public
certificate is present in our `ca` input, the connection will fail.

### The Ugly {#the-ugly}

We'll start with the outage here and then work our way backwards to understand
how the code and configuration got in a brittle and then broken state.
To tell the story of the outage, I'll introduce a fictional API and private
CA, but keep the core ideas intact. The API uses mutual TLS (mTLS)
to authenticate requests, so the the characters in the story are as follows:

-   **Server**: `https://api.acme.invalid`
-   **Server Root CA**: DigiCert[ref]DigiCert is one of the most
    reputable Certificate Authorities, if not **the** most reputable.[/ref]
-   **Client Root CA**: Acme Corp Legitimate Root CA

Both the server and client public certificate were signed by
intermediates[ref]As opposed to being directly signed by the root CA.[/ref]
as well:

```text
Root           CN: DigiCert High Assurance EV Root CA
  Intermediate CN: DigiCert SHA2 Extended Validation Server CA
    Leaf       CN: api.acme.invalid

Root           CN: Acme Corp Legitimate Root CA
  Intermediate CN: Acme Corp Production Intermediate CA
    Leaf       CN: 3975092b-4484-4b36-9f22-f84d4dd1e95a
```

In order to sign mTLS requests as the client, the TLS connection was configured
with a public certificate, a private key and a pair of
relevant CAs[ref]The astute observer may notice one CA is an intermediate
and the other is a root. This is not a typo, but is also not something
that is particularly correct. More on that later.[/ref]:

```typescript
const options: tls.SecureContextOptions = {
  key: fs.readFileSync(`${CONFIGURATION_DIR}/client-key.pem`),
  cert: fs.readFileSync(`${CONFIGURATION_DIR}/client-cert.pem`),
  ca: [
    fs.readFileSync(`${CONFIGURATION_DIR}/client-intermediate.pem`),
    fs.readFileSync(`${CONFIGURATION_DIR}/DigiCertHighAssuranceEVRootCA.crt.pem`),
  ],
}
```

Unfortunately, the `api.acme.invalid` certificate **expired** 23 months after
the code using this configuration was written and deployed. This is a textbook
case of "it works today, ship it" gone wrong. The service and API integration
worked perfectly fine for 22 months. Then, when Acme rotated the server
certificate, everything fell apart.

From Acme's perspective, nothing had changed about the `api.acme.invalid`
server because the new certificate was from DigiCert as well. As a result,
no communications or warnings were sent out to the API clients when the
certificate was rotated. However, DigiCert has **multiple** roots and the
new certificate was issued by a **different** CA certificate:

```text
Root           CN: DigiCert Global Root CA
  Intermediate CN: DigiCert TLS RSA SHA256 2020 CA1
    Leaf       CN: api.acme.invalid
```

Now the addition of `DigiCertHighAssuranceEVRootCA.crt.pem` to the `ca`
override provides no help. After the server certificate was rotated, a
`SELF_SIGNED_CERT_IN_CHAIN` error immediately started to occur on
**every request** to the Acme API[ref]This error indicates that the
CA &mdash; DigiCert Global Root CA &mdash; is not trusted by the custom `ca`
bundle override used by the application.[/ref]. Worse still, the on-call
engineer at the time had insufficient context on the original implementation
and had **never seen** this self-signed certificate error before. Combined
with the fact that Acme had not sent out change notifications, the code had
not changed and the service had not been redeployed recently, this sudden
outage was confounding.

Once the on-call engineer pulled in another team more familiar with
TLS, the error was clear but the source of the configuration was not.
Eventually, the `ca` override was found collaboratively and the API
integration was fixed by adding `DigiCertGlobalRootCA.crt.pem` to the `ca`
bundle override.

#### Why Override `ca` at All? {#why-override}

In sensitive or zero trust environments, it's common to use mutual TLS (mTLS).
Often in this scenario, an API provider will run a private CA and will use
it to sign [CSRs][3] for client certificates. When working with Acme Corp to
get a valid client certificate, the team generated a private key file
`client-key.pem` and sent off a CSR. Acme Corp gladly signed the CSR and sent
back the file `client-chain.pem`. This chain file contained both the public
certificate `3975092b-4484-4b36-9f22-f84d4dd1e95a` and the
Acme Corp Production Intermediate CA certificate.

The **name** of the `cert` option is what caused confusion and triggered the
brittle outage-inducing configuration. After a literal reading of the names
`cert` and `ca` in the TLS options, the team decided to split the up
`client-chain.pem` into two files:

```typescript
const options: tls.SecureContextOptions = {
  key: fs.readFileSync(`${CONFIGURATION_DIR}/client-key.pem`),
  cert: fs.readFileSync(`${CONFIGURATION_DIR}/client-cert.pem`),
  ca: [fs.readFileSync(`${CONFIGURATION_DIR}/client-intermediate.pem`)],
}
```

However, attempting to using this configuration during development failed
(as expected): `SELF_SIGNED_CERT_IN_CHAIN`[ref]The self-signed error occurs if
a server presents a **full** chain, i.e. leaf, intermediate and root. However,
it's more common for a server to only present a leaf and intermediate, in
which case the equivalent Node.js error would be
`UNABLE_TO_GET_ISSUER_CERT_LOCALLY`.[/ref].
This error is caused by the `ca` issue discussed [above](#the-bad): the root
DigiCert High Assurance EV Root CA was no longer trusted in the connection
because all of the default public root CAs have been replaced. In order to
solve this connection issue, the team [downloaded][4]
`DigiCertHighAssuranceEVRootCA.crt.pem` and added it to the `ca` override.

#### Could This Have Been Avoided? {#could-avoided}

If the team had used `client-chain.pem` directly, there would have been no need
to override the `ca` in the connection:

```typescript
const options: tls.SecureContextOptions = {
  key: fs.readFileSync(`${CONFIGURATION_DIR}/client-key.pem`),
  cert: fs.readFileSync(`${CONFIGURATION_DIR}/client-chain.pem`),
}
```

If **only** the leaf certificate[ref]The alternative to **only** the
leaf certificate is a chain file containing both the leaf certificate
and the intermediate CA that signed it.[/ref] is
used in the `cert` option, many servers will fail an mTLS request with
`UNABLE_TO_VERIFY_LEAF_SIGNATURE` or a similar error. This is because the
client party must present the leaf certificate **and** any intermediates
along the chain up to the root CA. The documentation for `cert`
[makes this clear][2]

> Cert chains in PEM format ... Each cert chain should consist of the PEM
> formatted certificate for a provided private key, followed by the PEM
> formatted intermediate certificates (if any), in order, and not including
> the root CA (the root CA must be pre-known to the peer, see `ca`).

Renaming the option from `cert` to `chain` in the `tls` package would be much
clearer. But the Node.js runtime and the standard library `tls` package have
**wide** usage and such a rename is likely impossible to pull off.

Once the intermediate CA is removed from the file used in `cert`, Node.js
can't hope to present the intermediate CA certificate during an mTLS handshake.
However, if the intermediate CA certificate is added via `ca`, Node.js can
find it in the root trust store and then present it to the server as the issuer
of the leaf.

#### Is the Server Certificate Rotation to Blame? {#rotation-blame}

> **TL;DR**: No

By design, X.509 certificates issued by public CAs expire often because they
have short lifetimes (typically [ninety days][8] to two years). Shorter
lifetimes require certificate and key rotations. Rotations help limit the
impact of key compromise and help make sure the public internet "upgrades" key
strength as technology improves.

### Takeaways {#takeaways}

> This is a textbook case of "it works today, ship it" gone wrong.

The connection option misuse described here was exacerbated by service
operators lacking familiarity with the class of errors typical when TLS
connections fail. But TLS is squarely one of those "here be dragons" topics for
most engineering teams (including information security teams). The takeaways
from this outage are not cut and dry:

-   It's unreasonable for every type of engineering team to have deep knowledge
    in this part of the stack, on-call service operators should **quickly**
    loop in teams or people that do have that knowledge during an outage
-   Teams that don't have deep knowledge of a given technology (e.g. TLS),
    should try to avoid "deep" customization when using it or try to share
    the burden of the complexity e.g. by using an auxiliary service provided
    by another team
-   Writing "tests" for things that work today but might break in the future
    is **very hard**. "Modern" software tooling is very good, but there
    are many kinds of assumptions that are just not possible to encode in
    unit tests or acceptance tests in today's landscape

<hr style="margin-bottom: 25px; width: 50%;">

[1]: /images/door-nowhere.jpg
[2]: https://nodejs.org/docs/latest-v14.x/api/tls.html#tls_tls_createsecurecontext_options
[3]: https://en.wikipedia.org/wiki/Certificate_signing_request
[4]: https://www.digicert.com/kb/digicert-root-certificates.htm
[6]: https://github.com/dhermes/ca-append-js
[7]: https://en.wiktionary.org/wiki/footgun
[8]: https://letsencrypt.org/2015/11/09/why-90-days.html
