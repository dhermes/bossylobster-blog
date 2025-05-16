---
title: AI-assisted Postgres schema surgery
description: This post describes a zero-downtime schema change to a high contention table &mdash; guided (and greatly accelerated) by ChatGPT.
date: 2025-05-15
author: Danny Hermes (dhermes@bossylobster.com)
tags: PostgreSQL, Migrations, ChatGPT, LLM
slug: ai-assisted-postgres-schema-surgery
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/postgres-schema-surgery-02.png
github_slug: content/2025-05-15-ai-assisted-postgres-schema-surgery.md
---

<div markdown="1" style="text-align: center;">
  ![lock-contention](/images/postgres-schema-surgery-hero.jpg)
</div>

> This is cross-posted from the WorkWhile engineering [blog][5].

This post describes a zero-downtime schema change to a high contention table
&mdash; guided (and greatly accelerated) by ChatGPT.

### Contents

- [We made the wrong assumption](#wrong-assumption)
- [Online migrations and table contention](#online-migrations)
- [I get by with a little help from my (AI) friend](#get-by-with-help)
- [Add new column](#add-new-column)
- [Constrain new column](#constrain-new-column)
- [Mirror writes](#mirror-writes)
- [Backfill](#backfill)
- [Validate mirrored data](#validate-mirrored-data)
- [Column (name) swap](#column-swap)
- [Say goodbye](#say-goodbye)
- [Migration (Alembic)](#migration-alembic)
- [Model changes (SQLAlchemy)](#model-changes-sqlalchemy)
- [Conclusion](#conclusion)

### We made the wrong assumption {#wrong-assumption}

On our (real) `address` table in the database, we put a constraint on the
`street` column directly in the definition: `street VARCHAR(50)`. (Yes we've
read the PostgreSQL ["Don't Do This"][1] wiki.) Unfortunately, a street being
capped at 50 characters is a falsehood programmers (may) [believe][2] about
addresses. We ran into legitimate data from a user with a length of 51:
**12345 Doctor Martin Luther King Junior Street North**[ref]OK not actually
12345, but a 5 digit street number![/ref] in St. Petersburg, FL.

We wanted to support this user, so we needed to relax this constraint and get
the data in the database. However, the `address` table is a high contention
table in our application: it receives a constant stream of reads and writes.
This makes it much more challenging to just change a column's type!

### Online migrations and table contention {#online-migrations}

<div markdown="1" style="text-align: center;">
  ![Lock contention](/images/postgres-schema-surgery-01.png)
</div>

In our application, we have active users at all times of the day. This means
there is no opportunity for taking downtime without impacting users. As a
result, we _strictly_ use **online migrations** for evolving our PostgreSQL
schema. This also allows our team to be nimble and make changes throughout the
workday to add new features or improve existing ones.

In order to resolve the character length issue, we needed to change the column
type of `street` (to either `VARCHAR(N>50)` or to `TEXT`). Changing the table
schema will always require an `ACCESS EXCLUSIVE` [lock][3], which means **all**
queries to the table will need to wait for the schema change to complete.

For a high contention table that receives multiple reads per second and close to
one write per second, an `ACCESS EXCLUSIVE` lock can cause the entire
application to stall. This is not acceptable to us or our users! Luckily, most
table schema changes resolve in a few microseconds after acquiring a lock due to
steady improvements in PostgreSQL over the last 15+ years.

However, changing a column's type is a special type of change: it may require a
full table rewrite. For a large table like `address`, a table rewrite is a very
long and costly operation, which would mean holding the `ACCESS EXCLUSIVE` lock
for a long time. Changing from a `VARCHAR(50)` to `TEXT` is a binary-coercible
column change and **should not** incur a full table rewrite on modern
PostgreSQL.

### I get by with a little help from my (AI) friend {#get-by-with-help}

Although the column types are binary-coercible, we wanted to be **VERY** sure
our application remained stable, so we chose to avoid[ref]Early in the process,
we attempted to change column type and kept getting timeouts, some of which
made slight impacts on application performance. This may very well have been
bad luck with lock contention. Rather than wait to find out, we elected to go
with the safer route and totally avoid the chance of a table rewrite.[/ref]
that and instead:

- Introduce a new column `street_new` with the correct type
- Add `CHECK` on `street_new` that can constrain text length but be more easily
  changed in the future without a column type change
- Copy data from `street` into the new column (in batches) and mirror writes
- Swap names after backfill is complete
- Drop the `street_new` column

I knew conceptually how to do all of this but I leaned heavily on ChatGPT to
just do all the actual work of writing DDL, SQLAlchemy, and Alembic code while I
did the **thinking**. Even as a daily user of LLM tools, I was really surprised
how perfectly ChatGPT nailed this and helped me go **really fast**:

<div markdown="1" style="text-align: center;">
  ![ChatGPT: Schema migration advice](/images/postgres-schema-surgery-02.png)
</div>

### Add new column {#add-new-column}

First step we'll add the new column. We elected to do this with DDL directly
rather than use Alembic migrations. This gave us the maximum level of control
while managing this sensitive change:

```sql
-- new-column.sql
SELECT NOW();

SET statement_timeout = '15s';
SET lock_timeout = '15s';

BEGIN;

ALTER TABLE public.address ADD COLUMN street_new TEXT;

COMMIT;

SELECT NOW();
```

Note that it's crucial that we cap the amount of time we're willing to wait on
and hold a lock as well as the total amount of time a statement will take.
Additionally, we print out before / after timestamps for auditing in case any
issues occur[ref]In future examples, we'll hide the `SELECT NOW()` and the
setting of timeouts but it's crucial to always track these when doing database
operations.[/ref].

```txt
workwhile> \i new-column.sql
You're about to run a destructive command.
Do you want to proceed? [y/N]: y
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 14:54:09.741308+00 |
+-------------------------------+
SELECT 1
SET
SET
BEGIN
ALTER TABLE
COMMIT
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 14:54:18.186533+00 |
+-------------------------------+
SELECT 1
Time: 9.035s (9 seconds), executed in: 9.027s (9 seconds)
```

### Constrain new column {#constrain-new-column}

Adding a `CHECK` constraint still requires an `ACCESS EXCLUSIVE` lock on the
table so we get it out of the way as soon as we can. (For large tables, it may
make more sense to add this constraint [as not valid][4] and then
`VALIDATE CONSTRAINT` after.)

```sql
-- add-length-constraint.sql
BEGIN;

ALTER TABLE public.address
  ADD CONSTRAINT street_length_check
  CHECK (CHAR_LENGTH(street_new) <= 60);

COMMIT;
```

Note that `CHAR_LENGTH(street_new)` refers to the new column but we want it to
refer to `street` when things are renamed and all said and done. Luckily
PostgreSQL will track this when the column gets renamed!

```txt
workwhile> \i add-length-constraint.sql
You're about to run a destructive command.
Do you want to proceed? [y/N]: y
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 14:58:42.280429+00 |
+-------------------------------+
SELECT 1
SET
SET
BEGIN
ALTER TABLE
COMMIT
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 14:58:47.972947+00 |
+-------------------------------+
SELECT 1
Time: 6.260s (6 seconds), executed in: 6.252s (6 seconds)
```

### Mirror writes {#mirror-writes}

In order to ensure that we can swap `street` and `street_new`, we need them both
to have the same data! To do this **WITHOUT** locking the table for an extended
period of time, we need to be able to backfill data in batches and ensure future
writes get mirrored to both columns. We can safely assume that `street_new`
**NEVER** receives writes directly: the application has only ever heard of
`street`.

```sql
-- add-trigger-to-table.sql
BEGIN;

CREATE OR REPLACE FUNCTION public.mirror_street_to_new()
RETURNS TRIGGER AS $$
BEGIN
  NEW.street_new := NEW.street;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_street_to_street_new
  BEFORE INSERT OR UPDATE ON public.address
  FOR EACH ROW
  EXECUTE FUNCTION public.mirror_street_to_new();

COMMIT;
```

It's important that `street_new` is a "stable" name[ref]Ask me how I know
this![/ref] in the `mirror_street_to_new()` function. After we swap the
columns, we'll leave the `sync_street_to_street_new` trigger in place to keep
the data in sync for final validation. So if `street_new` becomes an invalid
name, the function will begin to cause all writes to fail.

```txt
workwhile> \i add-trigger-to-table.sql
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 15:02:21.586163+00 |
+-------------------------------+
SELECT 1
SET
SET
BEGIN
CREATE FUNCTION
CREATE TRIGGER
COMMIT
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 15:02:22.011339+00 |
+-------------------------------+
SELECT 1
Time: 0.509s
```

### Backfill {#backfill}

Recall the primary reason we chose column mirroring was to avoid a table
rewrite. To that end, we need to backfill data into `street_new` in batches.
Luckily, we use `created_at` and `updated_at` metadata columns in **ALL** of our
tables so we can define batches based on most recent update. For example:

```sql
UPDATE
  public.address
SET
  street_new = street
WHERE
  '2022-10-01T00:00:00.000Z' <= updated_at
  AND updated_at < '2024-01-01T00:00:00.000Z';
```

The `updated_at` time is a **moving target** because addresses can be updated
during our backfill process. However, that's OK because any newer updates will
already be in sync due to our `sync_street_to_street_new` trigger.

### Validate mirrored data {#validate-mirrored-data}

After completing the backfill, we need to ensure that `street` and `street_new`
are identical. Note that `street = street_new` is not a sufficient predicate
because nulls will not compare equal with the `=` operator, so we use
`IS DISTINCT FROM`:

```txt
workwhile> SELECT
   COUNT(*)
 FROM
   public.address
 WHERE
   street IS DISTINCT FROM street_new;
+-------+
| count |
|-------|
| 0     |
+-------+
SELECT 1
Time: 0.207s
```

### Column (name) swap {#column-swap}

In order to swap `street` and `street_new`, we first need to rename `street` to
a different column name to enable the swap without both columns using the same
name at once:

```sql
-- swap-column-names.sql
BEGIN;

ALTER TABLE public.address
  RENAME COLUMN street TO street_old;
ALTER TABLE public.address
  RENAME COLUMN street_new TO street;
ALTER TABLE public.address
  RENAME COLUMN street_old TO street_new;

COMMIT;
```

Recall we want to continue to use the `street_new` name because at this point in
the migration, mirroring is still enabled and `mirror_street_to_new()` has a
"generic" (not table-specific) reference to `NEW.street_new`:

```txt
workwhile> \i swap-column-names.sql
You're about to run a destructive command.
Do you want to proceed? [y/N]: y
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 15:17:06.559432+00 |
+-------------------------------+
SELECT 1
SET
SET
BEGIN
ALTER TABLE
ALTER TABLE
ALTER TABLE
COMMIT
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 15:17:11.142957+00 |
+-------------------------------+
SELECT 1
Time: 5.279s (5 seconds), executed in: 5.271s (5 seconds)
```

### Say goodbye {#say-goodbye}

At this point, after a final validation,

```txt
workwhile> SELECT
   COUNT(*)
 FROM
   public.address
 WHERE
   street IS DISTINCT FROM street_new;
+-------+
| count |
|-------|
| 0     |
+-------+
SELECT 1
Time: 0.202s
```

we can stop mirroring and drop the `street_new` column:

```sql
-- drop-old-column.sql
BEGIN;

DROP TRIGGER sync_street_to_street_new ON public.address;

DROP FUNCTION public.mirror_street_to_new();

ALTER TABLE public.address
  DROP COLUMN street_new;

COMMIT;
```

Notice that dropping the column may take a slightly longer time than some of the
other migrations. However, the primary issue is getting a table lock (which is
highly variable depending on current application activity):

```txt
workwhile> \i drop-old-column.sql
You're about to run a destructive command.
Do you want to proceed? [y/N]: y
+-----------------------------+
| now                         |
|-----------------------------|
| 2025-04-24 15:23:36.9894+00 |
+-----------------------------+
SELECT 1
SET
SET
BEGIN
DROP TRIGGER
DROP FUNCTION
ALTER TABLE
COMMIT
+-------------------------------+
| now                           |
|-------------------------------|
| 2025-04-24 15:23:51.666602+00 |
+-------------------------------+
SELECT 1
Time: 15.139s (15 seconds), executed in: 15.130s (15 seconds)
```

### Migration (Alembic) {#migration-alembic}

Though we ran this migration via many small and careful steps, it's still useful
to document this step for future team members. Our team uses Alembic for the
large majority of migrations. (The raw DDL escape hatch is only necessary in
cases where we need to make a sensitive change that'll require locks that are
potentially problematic for the application.)

To document the change at a conceptual level:

```python
def upgrade():
    # 1. Change column type to TEXT
    op.alter_column(
        "address",
        "street",
        existing_type=sa.String(50),
        type_=sa.Text(),
        existing_nullable=True,
        schema="public",
    )

    # 2. Add CHECK constraint
    op.create_check_constraint(
        constraint_name="street_length_check",
        table_name="address",
        condition="CHAR_LENGTH(street) <= 60",
        schema="public",
    )


def downgrade():
    # 2. Remove CHECK constraint
    op.drop_constraint(
        constraint_name="street_length_check",
        table_name="address",
        type_="check",
        schema="public",
    )

    # 1. Revert column type to VARCHAR(50)
    op.alter_column(
        "address",
        "street",
        existing_type=sa.Text(),
        type_=sa.String(50),
        existing_nullable=True,
        schema="public",
    )
```

We always use `alembic stamp` to memorialize changes made outside of a typical
`alembic upgrade` operation:

```txt
$ date
Thu Apr 24 10:34:14 CDT 2025
$
$
$ uv run alembic stamp ef4486a350ee
INFO [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO [alembic.runtime.migration] Will assume transactional DDL.
INFO [alembic.runtime.migration] Running stamp_revision 146b1f84dda9 -> ef4486a350ee
$
$
$ date
Thu Apr 24 10:34:18 CDT 2025
```

### Model changes (SQLAlchemy) {#model-changes-sqlalchemy}

In addition to changing the `Column(TEXT)` in the model definition, the extra
`CHECK` constraint must be tracked in `__table_args__`:

```python
class Address(BaseModel):
    __table_args__ = (
        CheckConstraint("CHAR_LENGTH(street) <= 60", name="street_length_check"),
    )

    street = Column(TEXT)
    # ...
```

### Conclusion {#conclusion}

Fixing schema constraints in high contention tables like `address` is rarely
straightforward. But with a careful, methodical approach, it's absolutely
achievable without user-facing downtime. It's important to combine deep
understanding of PostgreSQL internals with thoughtful engineering practices like
online backfills and trigger-based mirroring. Just as importantly, it's a
reminder that tools like LLMs can meaningfully augment engineering workflows
&mdash; not by replacing decision-making, but by accelerating safe and accurate
implementation. Schema changes may always be risky, but they don't have to be
**scary**!

<div markdown="1" style="text-align: center;">
  ![Spooky DB](/images/postgres-schema-surgery-03.png)
</div>

[1]: https://wiki.postgresql.org/wiki/Don't_Do_This#Don.27t_use_varchar.28n.29_by_default
[2]: https://www.mjt.me.uk/posts/falsehoods-programmers-believe-about-addresses/
[3]: https://www.postgresql.org/docs/17/explicit-locking.html#LOCKING-TABLES
[4]: https://www.shayon.dev/post/2022/17/why-i-enjoy-postgresql-infrastructure-engineers-perspective/#adding-not-null-or-other-constraints
[5]: https://tech.workwhile.ai/blogs/ai-assisted-postgres-schema-surgery-p5hilaq7
