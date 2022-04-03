---
title: Running `vault` Locally
date: 2020-07-07
author: Danny Hermes (dhermes@bossylobster.com)
tags: Vault, Docker
slug: running-vault-locally
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2020-07-07-running-vault-locally.md
---

In order to run `vault` locally (I did this because I was on an airplane),
first start the server with a known root token

```console
export VAULT_TOKEN=root VAULT_ADDR=http://localhost:8200
vault server -dev -dev-root-token-id="${VAULT_TOKEN}"

vault version  # As a baseline, this is the version of `vault` I am using
# Vault v1.4.2 ('18f1c494be8b06788c2fdda1a4296eb3c4b174ce+CHANGES')
```

then replace the secrets engine with KVv1 (which is what we use at Blend at
the time of this writing)

```console
vault secrets disable secret
vault secrets enable -path=secret -version=1 kv
```

and finally seed any secrets that we'll use, for example

```console
vault write \
  secret/dev/service/deployment/cheese/default/BOARD_CREDENTIALS \
  value=joe@mail.invalid:s33krit
```

### Docker

If you don't have `vault` installed or want to avoid forgetting that you've
got a `vault` server running, you can use `docker`.

```console
docker run \
  --rm \
  --interactive --tty \
  --name vault-dev-server \
  --publish 8200:8200 \
  --cap-add IPC_LOCK \
  --env VAULT_DEV_ROOT_TOKEN_ID=root \
  vault:1.4.1
```

and then the same commands can be run to put it in KVv1 mode.
