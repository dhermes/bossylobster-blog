---
title: Setting Per-Connection Timeouts with TypeORM
date: 2021-08-24
author: Danny Hermes (dhermes@bossylobster.com)
tags: TypeORM, PostgreSQL
slug: typeorm-timeouts
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2021-08-24-typeorm-timeouts.md
---

### PostgreSQL Statement Timeout

For **most** applications that use a database, user-facing queries **must**
complete in a reasonable amount of time. In order to ensure a maximum
query time, PostgreSQL supports a `statement_timeout` which will cause a
query to be cancelled if it exceeds the timeout:

```text
$ psql
monsters_inc=> SHOW statement_timeout;
 statement_timeout
-------------------
 5s
(1 row)

monsters_inc=> SELECT pg_sleep(6);
ERROR:  canceling statement due to statement timeout
```

This value can be set on an existing connection or can be set
**globally** for a user:

```
$ psql
monsters_inc=> ALTER ROLE sully SET statement_timeout = '6s';
ALTER ROLE
monsters_inc=> SHOW statement_timeout;
 statement_timeout
-------------------
 0
(1 row)

monsters_inc=> \q
$
$ # Open new connection so default can take effect
$ psql
monsters_inc=> SHOW statement_timeout;
 statement_timeout
-------------------
 6s
(1 row)

monsters_inc=> \q
$
$ # Connection-level override
$ PGOPTIONS="-c statement_timeout=4s" psql
monsters_inc=> SHOW statement_timeout;
 statement_timeout
-------------------
 4s
(1 row)

monsters_inc=> \q
```

### Motivation

Setting a **global** statement timeout for a user **can** be a helpful
feature, but often is too much of a blunt object. For example, some types
of queries (e.g. migrations) may require a different timeout on a temporary
basis. Having the ability to use a connection-level timeout that **differs**
from a common / global one is likely a need that will come up during the
application development lifecycle.

Another common use case here is the need for two distinct "long running query"
and "user facing query" connection pools for the same application user.
Those two pools need different statement timeouts (given the types of queries)
so can't rely on a single global setting.

### Configuring TypeORM

Unfortunately, TypeORM tries to cover **many** database engines beyond
just PostgreSQL. As a result, there is no explicit TypeORM support for most
PostgreSQL run-time parameters. This is because these are specific to
PostgreSQL and don't generalize well to other support databases like MySQL.

A general purpose way of passing along any run-time parameter (e.g.
`statement_timeout` or `search_path` to specify a PostgreSQL schema) is to
use the `extra.options` field in the TypeORM connection options.

```typescript
import * as typeorm from "typeorm";

const OPTIONS: typeorm.ConnectionOptions = {
  name: "default",
  type: "postgres",
  host: "pg-shared.chimera.us-unicorn-3.rds.amazonaws.com",
  port: "5432",
  database: "monsters_inc",
  username: "sully",
  password: "s33krit",
  extra: {
    options: "-c statement_timeout=5500ms -c search_path=monsters",
  },
  entities: ["..."],
  migrations: ["..."],
};
```

### References

- GitHub issue [discussion][1] on `node-postgres` about setting named
  run-time parameters (e.g. `statement_timeout`)
- GitHub issue [discussion][2] on `typeorm` about setting `lock_timeout`

> **Caveat Emptor**: While I am describing a technique to improve the usage of
> TypeORM, this is not an endorsement of TypeORM or ORMs in general. I wrote
> this to address internal usage at Blend.

[1]: https://github.com/typeorm/typeorm/issues/3929#issuecomment-736096616
[2]: https://github.com/brianc/node-postgres/issues/983#issuecomment-736075608
