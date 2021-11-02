---
title: Remodeling the House While Living in It
description: Safely Renaming a Column in PostgreSQL
date: 2021-11-01
author: Danny Hermes (dhermes@bossylobster.com)
tags: Databases, Migrations, Rolling Update
slug: safe-column-renames
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/rename_created_at.jpg
github_slug: content/2021-11-01-safe-column-renames.md
---

![Rename Name Tag](/images/rename_created_at.jpg)

### Minor Mismatch

When using a database in an application, there are many ways the idioms from
the database ecosystem can disagree with the idioms in the programming language
used to write the application. The object-relational impedance [mismatch][1] is
one such example of this, but that is mostly about differences between
relational objects (i.e. rows in tables) and programming language type
systems.

Sometimes, the differences are just cosmetic. But this can still cause
issues with developer ergonomics, opportunities for subtle bugs or even lint
violations for codebases on the stricter side. Here I want to highlight the
specific issue when PostgreSQL column naming conventions disagree with field
naming conventions in JavaScript / TypeScript types.

### I Made a Mess

Consider the following TypeScript type for tracking issues in a ticketing
system:

```ts
import * as typeorm from 'typeorm';

@typeorm.Entity()
export class Ticket {
  @typeorm.PrimaryColumn({ type: 'uuid' })
  id!: number;

  @typeorm.Column()
  owner!: string;

  @typeorm.Column()
  description!: string;

  @typeorm.CreateDateColumn({ type: 'timestamp with time zone' })
  createdAt!: Date;

  @typeorm.UpdateDateColumn({ type: 'timestamp with time zone' })
  updatedAt!: Date;

  @typeorm.Column({ type: 'timestamp with time zone', nullable: true })
  resolvedAt?: Date;
}
```

<!--
CREATE TABLE "ticket" (
  "id" uuid NOT NULL,
  "owner" character varying NOT NULL,
  "description" character varying NOT NULL,
  "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  "resolvedAt" TIMESTAMP WITH TIME ZONE,

  CONSTRAINT "PK_d9a0835407701eb86f874474b7c" PRIMARY KEY ("id")
);

CREATE INDEX
  "IDX_4fd0fa28cf982e5252b358caa9"
ON
  "ticket" ("owner", "updatedAt");

INSERT INTO
  ticket (id, "owner", "description", "createdAt", "updatedAt", "resolvedAt")
VALUES
  ('9ca76412-6248-4928-bbf8-e4c32ccec193', 'bob@mail.invalid',  'Deprecate GET-form of DELETE',   '2021-10-22 13:31:48.467759+00', '2021-10-26 01:50:11.762684+00', NULL),
  ('3076d8bc-81b9-4f8e-af44-0b62493e1ff6', 'bev@mail.invalid',  'Implement protobuf parsing',     '2021-10-23 18:41:59.909022+00', '2021-10-23 18:41:59.909022+00', NULL),
  ('2a7eacd6-f758-4f9b-ab26-1c47cb2c009a', 'barb@mail.invalid', 'Compare DB purge strategies',    '2021-10-23 12:13:07.682559+00', '2021-10-27 07:45:13.110361+00', '2021-10-27 07:45:13.110361+00'),
  ('80c47584-0716-4952-8937-dd6af18d516b', 'bob@mail.invalid',  'Explicitly require API version', '2021-10-25 19:22:13.919551+00', '2021-10-25 19:22:13.919551+00', NULL);
-->

Using TypeORM with the defaults, a developer would end with a table of the
form:

```
tracker=> \d ticket
                         Table "tracker.ticket"
   Column    |           Type           | Collation | Nullable | Default
-------------+--------------------------+-----------+----------+---------
 id          | uuid                     |           | not null |
 owner       | character varying        |           | not null |
 description | character varying        |           | not null |
 createdAt   | timestamp with time zone |           | not null | now()
 updatedAt   | timestamp with time zone |           | not null | now()
 resolvedAt  | timestamp with time zone |           |          |
Indexes:
    "PK_d9a0835407701eb86f874474b7c" PRIMARY KEY, btree (id)
    "IDX_4fd0fa28cf982e5252b358caa9" btree (owner, "updatedAt")
```

Note the idiomatic JavaScript field names (`camelCase`) being directly ported
as column names. This causes problems when using them naively in PostgreSQL:

```psql
tracker=> SELECT owner, description, createdAt FROM ticket WHERE createdAt = updatedAt;
ERROR:  column "createdat" does not exist
LINE 1: SELECT owner, description, createdAt FROM ticket WHERE creat...
                                   ^
HINT:  Perhaps you meant to reference the column "ticket.createdAt".
```

A somewhat reasonable response to this may be "but TypeORM writes all my
queries". However, poking around in the database console (`psql` here)
**should** happen all the time, both during development and when evaluating
migrations, feature usage and performing other other one-off tasks. In order
to actually use the console, the columns need to be quoted to preserve the
casing:

```psql
tracker=> SELECT owner, description, "createdAt" FROM ticket WHERE "createdAt" = "updatedAt";
      owner       |          description           |           createdAt
------------------+--------------------------------+-------------------------------
 bev@mail.invalid | Implement protobuf parsing     | 2021-10-23 18:41:59.909022+00
 bob@mail.invalid | Explicitly require API version | 2021-10-25 19:22:13.919551+00
(2 rows)
```

This is not great. Due to PostgreSQL [handling][2] of identifiers, having
column names be all lowercase is the common convention. In order to
differentiate word boundaries, `snake_case` is a natural choice. For example
here we'd use `created_at` instead of `createdAt`.

### How Do I Get out of the Mess?

In TypeORM, a column rename is as simple as

```ts
  @typeorm.CreateDateColumn({ type: 'timestamp with time zone', name: 'created_at' })
  createdAt!: Date;
```

so we can just commit this and run the auto-generated migration? Right?
RIGHT? Maybe. But probably not. The generated migration is harmless enough:

```ts
await queryRunner.query(`ALTER TABLE "ticket" RENAME COLUMN "createdAt" TO "created_at"`);
```

However, there is almost always a need for migrations to be compatible with
both the "old code" and the "new code". The most common reason for this is to
enable fast rollbacks if the new code contains a defect. However, it's also
common for applications to be deployed with **rolling updates** or with
**blue green deploys**. In either case, the "old code" and the "new code" can
both be running at literally the same time. So whether it's rollback safety or
deployment strategy, it's easy to construct a strong argument that database
migrations can be applied with the currently running version of the code.

How does this come into play here? Renaming to `created_at` means that any
query in the currently running version of the code that references `createdAt`
would just break. At this point, we might just throw up our hands and regret
the fact that our columns have `camelCase` names. However,
[transactional DDL][3] and PostgreSQL [views][4] can save us here!

### The First Migration

We can create a view that **pretends** to be the `ticket` table while
maintaining the presented column names. Simultaneously, the underlying table
can rename the columns. (In order to make a view named `ticket`, we first
need to rename the table.) Doing any of these changes **alone** would represent
a broken state for the database, however PostgreSQL allows us to wrap all of
these DDL operations into a transaction!

The aforementioned changes require five statements:

```sql
-- Start a transaction
BEGIN;
-- Rename all the COLUMNs using `camelCase`
ALTER TABLE
  ticket
RENAME COLUMN
  "createdAt" TO created_at;
ALTER TABLE
  ticket
RENAME COLUMN
  "updatedAt" TO updated_at;
ALTER TABLE
  ticket
RENAME COLUMN
  "resolvedAt" TO resolved_at;
-- Rename the TABLE so that the VIEW can take its name
ALTER TABLE
  ticket
RENAME TO
  ticket_actual;
-- Create a VIEW to present the newly renamed column names, but also
-- present the new names
CREATE VIEW
  ticket AS
SELECT
  id,
  "owner",
  "description",
  created_at AS "createdAt",
  updated_at AS "updatedAt",
  resolved_at AS "resolvedAt",
  created_at,
  updated_at,
  resolved_at
FROM
  ticket_actual;
-- Commit the transaction
COMMIT;
```

To sanity check, notice that even after changing `ticket` to a view, reads
and writes continue to work:

```psql
tracker=> \d+ ticket
                                     View "tracker.ticket"
   Column    |            Type             | Collation | Nullable | Default | Storage  | Description
-------------+-----------------------------+-----------+----------+---------+----------+-------------
 id          | uuid                        |           |          |         | plain    |
...
View definition:
 SELECT ticket_actual.id,
    ticket_actual.owner,
...
   FROM ticket_actual;

tracker=> INSERT INTO
tracker->   ticket (id, "owner", "description", "createdAt", "updatedAt")
tracker-> VALUES
tracker->   (
tracker(>     '9ce77e1f-1390-4a9e-8142-dd5eb257b554',
tracker(>     'bev@mail.invalid',
tracker(>     'Vendor in 3rd party protobuf schema',
tracker(>     '2021-10-24 12:14:15.000173+00',
tracker(>     '2021-10-24 06:37:11.130880+00'
tracker(>   );
INSERT 0 1
tracker=> SELECT "owner", "description", "createdAt" FROM ticket;
       owner       |             description             |           createdAt
-------------------+-------------------------------------+-------------------------------
 bob@mail.invalid  | Deprecate GET-form of DELETE        | 2021-10-22 13:31:48.467759+00
 bev@mail.invalid  | Implement protobuf parsing          | 2021-10-23 18:41:59.909022+00
 barb@mail.invalid | Compare DB purge strategies         | 2021-10-23 12:13:07.682559+00
 bob@mail.invalid  | Explicitly require API version      | 2021-10-25 19:22:13.919551+00
 bev@mail.invalid  | Vendor in 3rd party protobuf schema | 2021-10-24 12:14:15.000173+00
(5 rows)

```

This migration can be coupled with a **code change** that starts to use the
newly introduced columns in the view: `created_at`, `updated_at` and
`resolved_at`. During the next deployment (when migrations also run), the
"old code" will use the old column names (which are now aliases in the view)
and the "new code" will use the new column names. Due to the way we've
structured the view, these are both compatible.
The `VIEW` and `TABLE` should be interchangeable to application
code[ref]Unless the code uses `SELECT *`, which may cause breakage due
to three new alias columns in the `VIEW`.[/ref].

### The Second Migration

Once the previous deploy has stabilized (i.e. we know it won't be rolled back)
we know the old column names `createdAt`, `updatedAt` and `resolvedAt` no
longer need to be kept around. As a result, we can remove the view and
restore the table back with its original name:

```sql
-- Start a transaction
BEGIN;
-- Remove the VIEW
DROP VIEW ticket;
-- Restore the TABLE to the original name
ALTER TABLE
  ticket_actual
RENAME TO
  ticket;
-- Commit the transaction
COMMIT;
```

All things being equal, application queries going through a `TABLE` instead
of a `VIEW` should be preferred. If a `VIEW` **can** be removed, it
should be as soon as possible. Relying on a `VIEW` in a codebase over a longer
time span can lead to inefficient queries caused by a mismatch between
developer assumptions about the exposed columns and the actual columns being
transformed in the view. The more complex the view is, the more likely this is
to be true.

### Conclusion

Transactional DDL allows to do things that would otherwise be impossible
to do without downtime. Combining this with PostgreSQL helpers for
separating storage from presentation, it's possible to make cosmetic renames
to tables and columns safely. It's **always** crucial to ensure migrations
can safely interact with the versions of the codebase immediately before and
after the migration is intended to run. The above approach shows a generic
approach that allows for surfacing "before and after" column views at the
same time. Relying on tools like TypeORM can provide a **lot** of value, but
they can also cause problems if automated outputs like migrations aren't
inspected closely.

<hr style="margin-bottom: 25px; width: 50%;">

[1]: https://en.wikipedia.org/wiki/Object%E2%80%93relational_impedance_mismatch
[2]: https://www.postgresql.org/docs/14/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
[3]: https://julien.danjou.info/why-you-should-care-that-your-sql-ddl-is-transactional/
[4]: https://www.postgresql.org/docs/14/sql-createview.html
