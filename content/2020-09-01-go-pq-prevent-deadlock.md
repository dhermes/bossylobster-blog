---
title: Preventing PostgreSQL Deadlocks in Go
description: Examples using Lock and Statement Timeouts
date: 2020-09-01
author: Danny Hermes (dhermes@bossylobster.com)
tags: Go, Golang, PostgreSQL
slug: go-pq-prevent-deadlock
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/Lock-Up-The-Forest.jpg
github_slug: content/2020-09-01-go-pq-prevent-deadlock.md
---

![All About Locks](/images/Lock-Up-The-Forest.jpg)

I've been writing a library for running PostgreSQL migrations in Go. One
of the primary pieces of advice I [keep][1] coming [across][2] is

> Beware of lock queues, use lock timeouts

In other words, each migration stage should happen **instantaneously** (or
almost instantaneously). For real-time applications, if a migration runs "for a
long time" it can potentially hold a lock that blocks every query in the
application. This post is about the mechanics of setting a `lock_timeout` in
PostgreSQL via the canonical `github.com/lib/pq` driver. I'll dive into how it
works, how it contrasts to equivalent connections via `psql` and we'll go
through four different deadlock scenarios that timeout.

### Contents

- [Prerequisites](#prerequisites)
- [Intentional Contention](#intentional-contention)
- [Example Set Up](#example-set-up)
- [Failures](#failures)
- `lock_timeout` [in the DSN](#lock-timeout-dsn)

### Prerequisites {#prerequisites}

<!-- For posterity

```
$ docker version
Client: Docker Engine - Community
 Version:           19.03.12
$
$ go version
go version go1.14 darwin/amd64
$
$ git --git-dir ${GOPATH}/src/github.com/lib/pq/.git log -1 --pretty=%H
ef080b6a8f499b5d60fe9f24a2f8a8beb671566d
$
$ git --git-dir ${GOPATH}/src/github.com/hashicorp/go-multierror/.git log -1 --pretty=%H
0d28cf682dbe774898e42a3db11b7ce24b36751a
$
$ git --git-dir ${GOPATH}/src/github.com/hashicorp/errwrap/.git log -1 --pretty=%H
7b00e5db719c64d14dd0caaacbd13e76254d02c0
```
-->

We'll be on a machine with Docker and Go installed. The Go packages
`github.com/lib/pq` and `github.com/hashicorp/go-multierror` should be
installed as well.

In order to run the examples, make sure a local `postgres` server is
running[ref]Take note of the connection parameters[/ref]:

```text
docker run \
  --detach \
  --hostname localhost \
  --publish 28007:5432 \
  --name dev-postgres-prevent-deadlock \
  --env POSTGRES_DB=superuser_db \
  --env POSTGRES_USER=superuser \
  --env POSTGRES_PASSWORD=testpassword_superuser \
  postgres:10.6-alpine
```

### Intentional Contention {#intentional-contention}

In order to introduce a deadlock, we borrow an example from
[When Postgres blocks: 7 tips for dealing with locks][1].
In the first transaction we update "hello" rows followed by "world" rows

```sql
BEGIN;
UPDATE might_deadlock SET counter = counter + 1 WHERE key = 'hello';
-- Sleep for 200ms
UPDATE might_deadlock SET counter = counter + 1 WHERE key = 'world';
COMMIT;
```

and in the second transaction we update the rows in the opposite order

```sql
BEGIN;
UPDATE might_deadlock SET counter = counter + 1 WHERE key = 'world';
-- Sleep for 200ms
UPDATE might_deadlock SET counter = counter + 1 WHERE key = 'hello';
COMMIT;
```

### Example Set Up {#example-set-up}

In order to trigger different failure modes, we allow two different
configurable durations:

- `lock_timeout` set directly in PostgreSQL (via `LOCK_TIMEOUT` environment
  variable)
- Timeout / deadline on a Go `context.Context` (via `CONTEXT_TIMEOUT`
  environment variable)

Additionally, we fix a third duration &mdash; the amount of time to sleep
between statements in each transaction &mdash; to 200 milliseconds.
By allowing the lock and context timeouts to vary, we can see a failure
manifest in (hopefully) an exhaustive set of scenarios.

Really we are concerned here with checking a few cases:

- What does `postgres` do when a lock is held for `lock_timeout` seconds?
- What does `postgres` do when a lock is held and a Go context is canceled?
- What does `postgres` do when left on its own (i.e. no lock or context
  timeout will relinquish the lock)?

The `pq-prevent-deadlock.go` [script][3] seeds the `might_deadlock` table
and then kicks off two simultaneous goroutines to intentionally cause
deadlock. The places in the script relevant to the discussion are the usage of
`lock_timeout` in the mostly hardcoded connection string (more on this
[later](#lock-timeout-dsn)):

```go
func createPool(ctx context.Context, cfg *Config) (*sql.DB, error) {
	dsnTemplate := "postgres://superuser:testpassword_superuser@localhost:28007/superuser_db?lock_timeout=%s&sslmode=disable"
	dsn := fmt.Sprintf(dsnTemplate, cfg.LockTimeout)
    pool, err := sql.Open("postgres", dsn)
    // ...
}
```

and the creation of a Go context that sets a deadline based on the context
timeout[ref]It's crucial that we pass this context in to every database
method that has a `Context`-accepting variant[/ref]:

```go
deadline := time.Now().Add(cfg.ContextTimeout)
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()
```

The deadlock itself happens in the function kicked off in the goroutines:

```go
func contendReads(ctx context.Context, wg *sync.WaitGroup, tx *sql.Tx, key1, key2 string, cfg *Config) error {
	defer wg.Done()

	updateRows := "UPDATE might_deadlock SET counter = counter + 1 WHERE key = $1;"
	_, err := tx.ExecContext(ctx, updateRows, key1)
	if err != nil {
		return err
	}

	time.Sleep(200 * time.Millisecond)
	_, err = tx.ExecContext(ctx, updateRows, key2)
	return err
}
```

### Failures {#failures}

#### Via `lock_timeout`

By setting `lock_timeout` to 10 milliseconds, much shorter than the 200
millisecond sleep between statements, we can induce [error][4]
`55P03: lock_not_available` directly from `postgres`:

```text
$ LOCK_TIMEOUT=10ms CONTEXT_TIMEOUT=600ms go run ./pq-prevent-deadlock.go
0.039350 Starting transactions
0.059424 Transactions opened
0.286993 Error(s):
0.287104 - &pq.Error{Severity:"ERROR", Code:"55P03", Message:"canceling statement due to lock timeout", Detail:"", Hint:"", Position:"", InternalPosition:"", InternalQuery:"", Where:"while updating tuple (0,1) in relation \"might_deadlock\"", Schema:"", Table:"", Column:"", DataTypeName:"", Constraint:"", File:"postgres.c", Line:"2989", Routine:"ProcessInterrupts"}
0.287119 - &pq.Error{Severity:"ERROR", Code:"55P03", Message:"canceling statement due to lock timeout", Detail:"", Hint:"", Position:"", InternalPosition:"", InternalQuery:"", Where:"while updating tuple (0,2) in relation \"might_deadlock\"", Schema:"", Table:"", Column:"", DataTypeName:"", Constraint:"", File:"postgres.c", Line:"2989", Routine:"ProcessInterrupts"}
```

This shows that (A) putting `lock_timeout` in the connection string used by
Go actually sets a timeout and (B) the database engine does the work of
canceling statements and providing a useful error to the client.

#### Force a Deadlock

By setting `lock_timeout` **and** the context timeout to 10 seconds, we can
leave `postgres` on its own to suffer with (and detect) the deadlock.
After less than two seconds the deadlock is detected and error
`40P01: deadlock_detected` is returned:

```text
$ LOCK_TIMEOUT=10s CONTEXT_TIMEOUT=10s go run ./pq-prevent-deadlock.go
0.043090 Starting transactions
0.058350 Transactions opened
1.276383 Error(s):
1.276474 - &pq.Error{Severity:"ERROR", Code:"40P01", Message:"deadlock detected", Detail:"Process 2385 waits for ShareLock on transaction 624; blocked by process 2384.\nProcess 2384 waits for ShareLock on transaction 625; blocked by process 2385.", Hint:"See server log for query details.", Position:"", InternalPosition:"", InternalQuery:"", Where:"while updating tuple (0,1) in relation \"might_deadlock\"", Schema:"", Table:"", Column:"", DataTypeName:"", Constraint:"", File:"deadlock.c", Line:"1140", Routine:"DeadLockReport"}
```

#### Go `context` Cancelation In Between Queries in a Transaction

By setting the context timeout to 100 milliseconds (half the length of the
sleep between statements), the transaction will be canceled **during** the
sleep which means the next statement will not even attempt to communicate
with `postgres`:

```text
$ LOCK_TIMEOUT=10s CONTEXT_TIMEOUT=100ms go run ./pq-prevent-deadlock.go
0.049146 Starting transactions
0.060474 Transactions opened
0.268488 Error(s):
0.268542 - context.deadlineExceededError{}
0.268547 - context.deadlineExceededError{}
```

#### Cancel "Stuck" Deadlock via Go context Cancelation

Setting the context timeout to 600 milliseconds is long enough that the sleep
between statements completes but not so long that `postgres` detects the
deadlock. In this case a `57014: query_canceled` is returned:

```text
$ LOCK_TIMEOUT=10s CONTEXT_TIMEOUT=600ms go run ./pq-prevent-deadlock.go
0.037892 Starting transactions
0.048328 Transactions opened
0.610551 Error(s):
0.610640 - &pq.Error{Severity:"ERROR", Code:"57014", Message:"canceling statement due to user request", Detail:"", Hint:"", Position:"", InternalPosition:"", InternalQuery:"", Where:"while updating tuple (0,1) in relation \"might_deadlock\"", Schema:"", Table:"", Column:"", DataTypeName:"", Constraint:"", File:"postgres.c", Line:"3026", Routine:"ProcessInterrupts"}
0.610663 - &pq.Error{Severity:"ERROR", Code:"57014", Message:"canceling statement due to user request", Detail:"", Hint:"", Position:"", InternalPosition:"", InternalQuery:"", Where:"while updating tuple (0,2) in relation \"might_deadlock\"", Schema:"", Table:"", Column:"", DataTypeName:"", Constraint:"", File:"postgres.c", Line:"3026", Routine:"ProcessInterrupts"}
```

This is somewhat of a pleasant surprise because the in-flight statement:

```go
time.Sleep(200 * time.Millisecond)
_, err = tx.ExecContext(ctx, updateRows, key2)
```

might very well be expected to block indefinitely. Instead, an event loop
in `github.com/lib/pq` detects the context cancelation and manages to
communicate the canceled query to `postgres` as well.

### `lock_timeout` in the DSN {#lock-timeout-dsn}

Though `lock_timeout` is directly supported in the connection string in
`github.com/lib/pq`, it's [explicitly][5] **not** supported in
`psql` / `libpq`:

```text
$ psql "postgres://superuser:testpassword_superuser@localhost:28007/superuser_db?lock_timeout=10ms&sslmode=disable"
psql: error: could not connect to server: invalid URI query parameter: "lock_timeout"
```

Instead `github.com/lib/pq` parses all query parameters when [reading a DSN][6]
and then passes all non-driver settings through as key-value pairs when
[forming a startup packet][7]. There are 13[ref]Though 13 are supported by
`github.com/lib/pq`, there are 29 `postgres` [parameter keywords][5][/ref]
designated driver settings [supported by][8] `github.com/lib/pq`: `host`,
`port`, ..., etc.

#### What's the `psql` Equivalent?

From the [Start-up][9] section of the documentation for
"Frontend/Backend Protocol > Message Flow", we see

> To begin a session, a frontend opens a connection to the server and sends a
> startup message ... (Optionally, the startup message can include additional
> settings for run-time parameters.)

Using `PGOPTIONS="-c {key}={value}"` with `psql` enables [setting][10]
named run-time parameters[ref]It's also worth noting that `github.com/lib/pq`
is `PGOPTIONS`-[aware][11][/ref]:

```text
$ PGOPTIONS="-c lock_timeout=10ms" psql "postgres://superuser:testpassword_superuser@localhost:28007/superuser_db?connect_timeout=5&sslmode=disable"
...
superuser_db=# SHOW lock_timeout;
 lock_timeout
--------------
 10ms
(1 row)

superuser_db=# \q
```

[1]: https://www.citusdata.com/blog/2018/02/22/seven-tips-for-dealing-with-postgres-locks/
[2]: https://benchling.engineering/move-fast-and-migrate-things-how-we-automated-migrations-in-postgres-d60aba0fc3d4
[3]: /code/pq-prevent-deadlock.go
[4]: https://www.postgresql.org/docs/10/errcodes-appendix.html
[5]: https://www.postgresql.org/docs/10/libpq-connect.html#LIBPQ-PARAMKEYWORDS
[6]: https://github.com/lib/pq/blob/v1.8.0/connector.go#L67-L69
[7]: https://github.com/lib/pq/blob/v1.8.0/conn.go#L1093-L1105
[8]: https://github.com/lib/pq/blob/v1.8.0/conn.go#L1058-L1084
[9]: https://www.postgresql.org/docs/10/protocol-flow.html#id-1.10.5.7.3
[10]: https://www.postgresql.org/docs/10/app-postgres.html#id-1.9.5.13.6.3
[11]: https://github.com/lib/pq/blob/v1.8.0/conn.go#L1945-L1946
