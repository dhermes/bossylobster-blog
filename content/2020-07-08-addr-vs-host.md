---
title: `ADDR` vs. `HOST`
date: 2020-07-08
author: Danny Hermes (dhermes@bossylobster.com)
tags: Configuration, SOA
slug: addr-vs-host
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2020-07-08-addr-vs-host.md
---

> **TL;DR**: Prefer inclusion of the protocol in configurable environment
> variables
>
> `VAULT_ADDR=https://vault.sandbox.invalid:8200`
>
> over
>
> `VAULT_HOST=vault.sandbox.invalid`
>
> since this enables targeting a local server, e.g. `http://localhost:8200`
> without any code changes.

We utilize sandbox, staging and other siloed environments to test changes
before they go to production. As a result, this means application code and
library code often needs to have hostnames that are configurable based on the
current environment. For example:

```typescript
// config.ts
import * as process from "process";

export const VAULT_HOST = process.env.VAULT_HOST || "vault.sandbox.invalid";
```

Once the hostname is specified, it's common to use it to form a base URL
or to form fully fledged URLs:

```typescript
// auth.ts
import * as secrets from "some-internal-secrets-library";

import * as config from "./config";

export const CLIENT = new secrets.Client(`https://${config.VAULT_HOST}:8200`);
```

However, this approach **requires** the full address to use the `https`
protocol. In deployed environments, this isn't a problem because we **want**
to be communicating over TLS / `https`. However, the `*_HOST` approach leaves
no room for swapping out for a locally running version of the given
dependency: `http://localhost:*`. (See [Running `vault` Locally][1] for
an explanation of **how** to run such a dependency locally.)

When doing local development in one application it may be necessary to also run
a related application locally. (Even if not necessary, it can be quite
convenient, e.g. if doing development on an airplane or without internet
access.) To support this, the `*_ADDR` pattern can be used instead of the
`*_HOST` pattern:

```typescript
// config.ts
import * as process from "process";

export const VAULT_HOST = process.env.VAULT_HOST || "vault.sandbox.invalid";
export const VAULT_ADDR =
  process.env.VAULT_ADDR || `https://${VAULT_HOST}:8200`;
// auth.ts
import * as secrets from "some-internal-secrets-library";

import * as config from "./config";

export const CLIENT = new secrets.Client(config.VAULT_ADDR);
```

[1]: /2020/07/running-vault-locally.html
