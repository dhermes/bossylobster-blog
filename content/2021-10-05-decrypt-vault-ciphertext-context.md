---
title: Decrypting Vault Ciphertext with a Context
description: Mechanics of Vault Derived Keys
date: 2021-10-05
author: Danny Hermes (dhermes@bossylobster.com)
tags: Hashicorp, Vault, Encryption, Key Derivation
slug: decrypt-vault-ciphertext-context
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/Vault_PrimaryLogo_Black_RGB.png
github_slug: content/2021-10-05-decrypt-vault-ciphertext-context.md
---

In a previous [post][1], I described a use case for customer provided keys
with Vault. One of the implications of this was the need for decryption after a
bulk data export. In that post, I gave a concrete example of decrypting Vault
ciphertext **directly** with a customer provided key. However, it's also
very common to encrypt using a derived key, created with a
**user-supplied context**. In this post, we'll give a concrete example of
generating a derived key and then decrypting Vault ciphertext with it.

### Initialize {#initialize}

First, start a test Vault instance with transit encryption enabled:

```text
$ docker run \
>   --rm \
>   --detach \
>   --name vault-dev-server \
>   --publish 8200:8200 \
>   --cap-add IPC_LOCK \
>   --env VAULT_DEV_ROOT_TOKEN_ID=root \
>   vault:1.8.3
$
$ export VAULT_TOKEN=root VAULT_ADDR=http://localhost:8200
$ vault secrets enable transit
Success! Enabled the transit secrets engine at: transit/
```

Then simulate a customer provided key and **require** that a user-supplied
context must always be used by setting `derived=true`:

```text
$ vault write transit/keys/acme-co-provided \
>   type=aes256-gcm96 \
>   allow_plaintext_backup=true \
>   exportable=true \
>   derived=true
Success! Data written to: transit/keys/acme-co-provided
```

### Encrypt Data {#encrypt-data}

If we try to encrypt **without** a context, it will fail since key derivation
is required:

```text
$ echo -n 'FOO' | base64
Rk9P
$ vault write transit/encrypt/acme-co-provided plaintext=Rk9P
Error writing data to transit/encrypt/acme-co-provided: Error making API request.

URL: PUT http://localhost:8200/v1/transit/encrypt/acme-co-provided
Code: 400. Errors:

* missing 'context' for key derivation; the key was created using a derived
  key, which means additional, per-request information must be included in order
  to perform operations with the key
```

Instead, we encrypt the data with the context `{"bar":"baz"}`:

```text
$ echo -n '{"bar":"baz"}' | base64
eyJiYXIiOiJiYXoifQ==
$ vault write transit/encrypt/acme-co-provided plaintext=Rk9P context=eyJiYXIiOiJiYXoifQ==
Key            Value
---            -----
ciphertext     vault:v1:1pEqzFnkQEa5RA35ynhOd0Ye907S9PvWIq5dRPDP3Q==
key_version    1
```

### Read Key Inputs {#read-key-inputs}

First, take note of the key derivation function used and the key type:

```text
$ vault read transit/keys/acme-co-provided
Key                       Value
---                       -----
...
kdf                       hkdf_sha256
...
type                      aes256-gcm96
```

Then, export the key via the backup API:

```text
$ vault read transit/backup/acme-co-provided
Key       Value
---       -----
backup    eyJwb2xpY3kiOnsibmFtZS...
$
$ vault read --field=backup transit/backup/acme-co-provided | base64 --decode | jq
{
  "policy": {
    "name": "acme-co-provided",
    "keys": {
      "1": {
        "key": "rph2pwTQCx+TD/lk+7o9igzQw5A7FU3+S+Z24Cf9Duk=",
        ...
      }
    },
    ...
  },
  ...
}
```

### Decrypt Ciphertext {#decrypt-ciphertext}

<!-- Uses `cryptography@35.0.0` -->

With the key, algorithms and ciphertext in hand, we are ready to decrypt.
First, create a derived key using the context:

```python
>>> import cryptography.hazmat.primitives.hashes
>>> algorithm = cryptography.hazmat.primitives.hashes.SHA256()
>>>
>>> import cryptography.hazmat.backends
>>> backend = cryptography.hazmat.backends.default_backend()
>>>
>>> import base64
>>> context = base64.b64decode(b"eyJiYXIiOiJiYXoifQ==")
>>> context
b'{"bar":"baz"}'
>>>
>>> import cryptography.hazmat.primitives.kdf.hkdf
>>> hkdf = cryptography.hazmat.primitives.kdf.hkdf.HKDF(
...     algorithm=algorithm, length=32, info=context, backend=backend, salt=None
... )
>>>
>>> key = base64.b64decode("rph2pwTQCx+TD/lk+7o9igzQw5A7FU3+S+Z24Cf9Duk=")
>>> derived_key = hkdf.derive(key)
>>> len(derived_key)
32
>>> derived_key
b'uU\x18\xdf...'
```

Then, decrypt the ciphertext with the derived key:

```python
>>> encoded = "1pEqzFnkQEa5RA35ynhOd0Ye907S9PvWIq5dRPDP3Q=="
>>> iv_and_ciphertext = base64.b64decode(encoded)
>>> iv_bytes = iv_and_ciphertext[:12]
>>> ciphertext_bytes = iv_and_ciphertext[12:]
>>>
>>> import cryptography.hazmat.primitives.ciphers.aead
>>> aead_cipher = cryptography.hazmat.primitives.ciphers.aead.AESGCM(derived_key)
>>> aead_cipher.decrypt(iv_bytes, ciphertext_bytes, None)
b'FOO'
```

[1]: /2021/07/vault-import.html
