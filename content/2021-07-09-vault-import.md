---
title: Importing External Keys into Vault
description: Synthetic Backups and Offsite Decryption
date: 2021-07-09
author: Danny Hermes (dhermes@bossylobster.com)
tags: Hashicorp, Vault, Import, Encryption
slug: vault-import
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/Vault_PrimaryLogo_Black_RGB.png
github_slug: content/2021-07-09-vault-import.md
---

![Vault](/images/Vault_PrimaryLogo_Black_RGB.png)

### Contents

-   [Motivation](#motivation)
-   ["Importing" via Restore](#importing-via-restore)
-   [Decrypting Exported Ciphertext](#decrypting-exported-ciphertext)
-   [Key Backup Format](#key-backup-format)

### Motivation {#motivation}

To understand why it's helpful to import external keys into Vault, it's
important to understand

-   How and why encrypted data is stored in databases
-   How Vault provides features that aid in encrypting and decrypting data
-   Reasons for data export and potential consumers of exported data

When storing PII and other sensitive information in a database, a common
best practice is to first **encrypt** the data before storing it.
For example, in a `users` table in an RDBMS, the social security number
(`ssn`) is sensitive but other columns can be stored in cleartext. Encryption
can be done with homegrown schemes that utilize a (very sensitive) primary key
on a per-application basis. However, this doesn't scale well in medium to
large companies where there are **many** databases and applications, all with
a similar need.

This is where HashiCorp [Vault][1] comes in. With a single instance of Vault,
an entire organization can utilize a centralized store for secrets and
an interface for encrypting and decrypting data. Access to these features can
be tightly controlled via the use of policies, e.g. if two applications want to
share access to the same secrets or encryption keys. A core design
consideration for Vault is that all keys used for encryption remain
"contained" within. Key export is **possible** but must be explicitly opted
into.

The last piece of the puzzle here is data export. In multitenant architectures,
data is often divided by customer via logical or physical segmentation. A given
customer may want an export of their data, e.g. for performing an
audit. In a **raw** database dump of the customer's data, all of the sensitive
fields (stored as ciphertext) would be essentially missing. If the data size is
large enough, manually decrypting **every** piece of sensitive data may take
too long or put too large of a strain on Vault to be worth it. This is where
the demand for a **customer provided key** comes in. If the customer already
owns the root key used to encrypt their data, then ciphertext in a raw dump
could be decrypted **after** a data export.

### "Importing" via Restore {#importing-via-restore}

There is no **official** way to import external keys into Vault, but this
feature can be approximated. Vault provides a backup and restore mechanism on
a per-key basis and this can be used to "restore" a synthetic backup
constructed from a customer provided key[ref]It should be noted that
this goes **against** one of the design considerations of Vault, i.e.
that keys are generated internally and are never exposed outside of
Vault.[/ref].

As an example here, a synthetic backup of an `aes256-gcm96` key will be
created. See [Key Backup Format](#key-backup-format) for more details on how
to construct a synthetic backup. This means 32 bytes[ref]The secret key is
32 bytes (or 256 bits) since the scheme used is `aes256-gcm96`.[/ref] are
needed for the key, base64 encoded for JSON:

```json
{
  "policy": {
    "name": "acme-co-provided",
    "type": 0,
    "keys": {
      "1": {
        "key": "MoUxGpXXLY1GpicsJG4FFCSp/t6HzVVlddS+CIbEJyE=",
        "hmac_key": null,
        "time": "2021-07-08T18:21:51.080371000Z",
        // ...
      }
    },
    // ...
  }
}
```

Once the backup is constructed, the [restore][2] API should be used with
the backup as a base64 encoded field:

```text
$ BACKUP_B64="$(cat backup.json | base64)"
$ vault write transit/restore/acme-co-provided backup="${BACKUP_B64}"
Success! Data written to: transit/restore/acme-co-provided
```

### Decrypting Exported Ciphertext {#decrypting-exported-ciphertext}

For a given party with a **known** key, decrypting ciphertext outside of Vault
is the primary goal of providing an external key. As an example, consider
the ciphertext produced when encrypting the secret text `FOO`:

```text
$ echo -n FOO | base64
Rk9P
$
$ vault write transit/encrypt/acme-co-provided plaintext=Rk9P
Key            Value
---            -----
ciphertext     vault:v1:aMEvW33l8iXqoDcvXl8KTtkaJEVcB8yeSsQ69mOltw==
key_version    1
```

The encrypted content comes after the header `vault:v1:`, which in this
case is 31 bytes base64 encoded. Of these, the [first 12][4] bytes[ref]The IV
is 12 bytes (or 96 bits) since the scheme used is `aes256-gcm96`.[/ref]
are the initialization vector (IV):

```python
>>> import base64
>>>
>>> encoded = "aMEvW33l8iXqoDcvXl8KTtkaJEVcB8yeSsQ69mOltw=="
>>> iv_and_ciphertext = base64.b64decode(encoded)
>>> iv_bytes = iv_and_ciphertext[:12]
>>> ciphertext_bytes = iv_and_ciphertext[12:]
```

Using the key from `backup.json` and the excellent Python `cryptopgraphy`
[package][3], this ciphertext can be decomposed and decrypted:

```python
>>> key_bytes = base64.b64decode("MoUxGpXXLY1GpicsJG4FFCSp/t6HzVVlddS+CIbEJyE=")
>>>
>>> import cryptography.hazmat.primitives.ciphers.aead
>>> aead_cipher = cryptography.hazmat.primitives.ciphers.aead.AESGCM(key_bytes)
>>> aead_cipher.decrypt(iv_bytes, ciphertext_bytes, None)
b'FOO'
```

For larger ciphertext (e.g. for an encrypted PDF file), it may be desired to
do streaming decryption instead of using `aead.AESGCM`. In this case, it's
crucial to know that the **last** 16 bytes are the authentication tag:

```python
>>> import cryptography.hazmat.primitives.ciphers.algorithms
>>> algorithm = cryptography.hazmat.primitives.ciphers.algorithms.AES(key_bytes)
>>>
>>> import cryptography.hazmat.primitives.ciphers.modes
>>> tag = ciphertext_bytes[-16:]
>>> mode = cryptography.hazmat.primitives.ciphers.modes.GCM(iv_bytes, tag=tag)
>>>
>>> import cryptography.hazmat.primitives.ciphers
>>> cipher = cryptography.hazmat.primitives.ciphers.Cipher(algorithm, mode=mode)
>>> decryptor = cipher.decryptor()
>>> decryptor.update(ciphertext_bytes[:-16])  # Do not include `tag`
b'FOO'
>>> decryptor.finalize()
b''
```

### Key Backup Format {#key-backup-format}

To construct a synthetic backup, it's necessary to understand the format of
the backup JSON. To inspect an existing one, create an exportable key:

```text
$ vault write transit/keys/acme-co-provided \
>   type=aes256-gcm96 allow_plaintext_backup=true exportable=true
Success! Data written to: transit/keys/acme-co-provided
$
$ vault read transit/keys/acme-co-provided
Key                       Value
---                       -----
allow_plaintext_backup    true
deletion_allowed          false
derived                   false
exportable                true
keys                      map[1:1625786511]
latest_version            1
min_available_version     0
min_decryption_version    1
min_encryption_version    0
name                      acme-co-provided
supports_decryption       true
supports_derivation       true
supports_encryption       true
supports_signing          false
type                      aes256-gcm96
```

and then export the key:

```text
$ vault read transit/backup/acme-co-provided
Key       Value
---       -----
backup    eyJwb2xp...
```

Once exported, the `backup` value can be base64 decoded and will resemble
the JSON snippet [above](#importing-via-restore). For more details on the
fields, see the underyling Go [struct][5].

[1]: https://www.vaultproject.io/
[2]: https://www.vaultproject.io/api/secret/transit#restore-key
[3]: https://cryptography.io/en/latest/
[4]: https://discuss.hashicorp.com/t/what-is-the-vault-ciphertext-format-in-case-i-want-to-parse-it/3574/2
[5]: https://github.com/hashicorp/vault/blob/v1.7.3/sdk/helper/keysutil/policy.go#L302
