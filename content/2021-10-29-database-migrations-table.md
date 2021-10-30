---
title: The Case for a Metadata Table for Database Migrations
description: Arguments for Running Exactly Once
date: 2021-10-29
author: Danny Hermes (dhermes@bossylobster.com)
tags: Databases, Migrations
slug: database-migrations-table
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/Legal_pad_and_pencil.jpg
github_slug: content/2021-10-29-database-migrations-table.md
---

![Tracking Migrations](/images/Legal_pad_and_pencil.jpg)

### Motivation {#motivation}

As features are added, changed or deleted, the data model used by an
application usually changes as well. For most database-backed applications,
this means migrations are needed.

With this in mind, the fundamental goal of database migrations:

> The current database schema should match the currently running code.

However, achieving this goal is not so easy. A typical database migration
might be adding an index to improve performance of a common query:

```sql
CREATE INDEX
  idx_books_publish_date
ON
  books (publish_date DESC, title ASC);
```

or adding a new column to support a new feature set:

```sql
ALTER TABLE
  books
ADD COLUMN
  latest_edition TIMESTAMP;
```

In PostgreSQL, migrations like these are easy to write in an idempotent way

```sql
CREATE INDEX IF NOT EXISTS
  idx_books_publish_date
ON
  books (publish_date DESC, title ASC);
---
ALTER TABLE
  books
ADD COLUMN IF NOT EXISTS
  latest_edition TIMESTAMP;
```

But not all migrations are so simple. Some migrations involve backfilling
information:

```sql
UPDATE
  books
SET
  latest_edition = publish_date;
```

and running a migration like that multiple times would be problematic (e.g.
if the data has already been backfilled and the new code allows `publish_date`
and `latest_edition` to start to diverge).

This is where a metadata table for migrations comes in. By keeping a clear
record of which migrations were run (and when), we can ensure each migration
will be run **exactly once** during development and more crucially, in
production databases.

### Guards {#guards}

One alternative to a migrations table: introduce queries that check if a
migration was already performed and **guard** against running it twice.

Some arguments against this strategy:

-   Doing this for **every migration** introduced in the codebase is a lot of
    extra work
-   This introduces an opportunity to make mistakes by writing buggy guards;
    for teams with a mix of experienced and inexperienced database users,
    writing guards **correctly** represents a real challenge
-   In order to do "exactly once" checks on some migrations (e.g. the backfill
    one above), it may be necessary to introduce **phantom** columns to the
    database as breadcrumbs indicating the migration occurred

```sql
UPDATE
  books
SET
  latest_edition = publish_date,
  latest_edition_backfill = TRUE
WHERE
  latest_edition_backfill = FALSE;
```

-   Application invariants may change over time and invalidate guards that
    were historically correct

### In Practice {#in-practice}

It's useful to have an example to understand **how** a migrations table is
constructed and how it fits into development and deployment. I'll use the
example migrations from my `golembic` [tool][1] as our example.

To get started, the development database needs to be running. In this stage,
there should be no tables yet because no migrations have run:

```text
$ make start-postgres
Network dev-network-golembic created.
Container dev-postgres-golembic started on port 18426.
...
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                     NAMES
480e5fce3e10   postgres:13.1-alpine   "docker-entrypoint.s…"   54 seconds ago   Up 52 seconds   0.0.0.0:18426->5432/tcp   dev-postgres-golembic
$
$ make psql
Running psql against port 18426
psql "postgres://golembic_admin:testpassword_admin@127.0.0.1:18426/golembic"
...
golembic=> \dt
Did not find any relations.
golembic=> \q
```

Using `golembic`, we can run the migrations in the development database:

```text
$ make run-postgres-cmd
Applying c9b52448285b: Create users table
Applying f1be62155239: Seed data in users table
Applying dce8812d7b6f: Add city column to users table
Applying 0430566018cc: Rename the root user [MILESTONE]
Applying 0501ccd1d98c: Add index on user emails (concurrently)
Applying e2d4eecb1841: Create books table
Applying 432f690fcbda: Create movies table
```

At this point, the migrations will have created the three tables needed by
the application: `books`, `movies` and `users`. Observe via `make psql`:

```psql
golembic=> \dt
                   List of relations
 Schema |        Name         | Type  |     Owner
--------+---------------------+-------+----------------
 public | books               | table | golembic_admin
 public | golembic_migrations | table | golembic_admin
 public | movies              | table | golembic_admin
 public | users               | table | golembic_admin
(4 rows)

```

In addition to the application tables from the migrations, there is also a
new metadata table `golembic_migrations`. This contains a record of the
migrations that have already been run:

```psql
golembic=> SELECT * FROM golembic_migrations;
 serial_id |   revision   |   previous   |          created_at
-----------+--------------+--------------+-------------------------------
         0 | c9b52448285b |              | 2021-10-29 03:57:57.92535+00
         1 | f1be62155239 | c9b52448285b | 2021-10-29 03:57:57.936784+00
         2 | dce8812d7b6f | f1be62155239 | 2021-10-29 03:57:57.945764+00
         3 | 0430566018cc | dce8812d7b6f | 2021-10-29 03:57:57.954536+00
         4 | 0501ccd1d98c | 0430566018cc | 2021-10-29 03:57:57.963776+00
         5 | e2d4eecb1841 | 0501ccd1d98c | 2021-10-29 03:57:57.986174+00
         6 | 432f690fcbda | e2d4eecb1841 | 2021-10-29 03:57:57.9968+00
(7 rows)

golembic=> \q
```

Using this record, the **next time** the migrations command runs, the
records in `golembic_migrations` can be used to determine that no new
migrations need to run:

```text
$ make run-postgres-cmd
No migrations to run; latest revision: 432f690fcbda
```

### Prior Art {#prior-art}

Although it may seem like an advertisment for `golembic`, the point of this
post was to make a case for a migrations table. To see `golembic` isn't
alone, note that [TypeORM][2] takes a similar approach. For example:

```psql
dunder_mifflin=> SELECT * FROM migrations;
 id |   timestamp   |                     name
----+---------------+-----------------------------------------------
  1 | 1568674788742 | initial1568674788742
  2 | 1571783618350 | recipient1571783618350
  3 | 1572313444993 | recipientEnum1572313444993
  4 | 1572479127851 | ticket1572479127851
  5 | 1572990972108 | ticketIndex1572990972108
  6 | 1573594420208 | uniqueConstraint1573594420208
(6 rows)

dunder_mifflin=> \q
```

(There are lots of ORMs and migrations tools other than TypeORM that also take
the same approach, I just had this example handy.)

[1]: https://github.com/dhermes/golembic/tree/2021.10.29
[2]: https://github.com/typeorm/typeorm
