---
title: What Is a Milestone Migration and Why Do I Care?
description: Special Migrations in the Presence of Rolling Updates
date: 2021-10-30
author: Danny Hermes (dhermes@bossylobster.com)
tags: Databases, Migrations, Milestone
slug: database-migrations-milestone
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/database_milestone.jpg
github_slug: content/2021-10-30-database-migrations-milestone.md
---

![Database Milestone](/images/database_milestone.jpg)

### Motivation {#motivation}

Over time an application becomes a living thing. When operating a running
service, it's crucial to not only ask the question

> Does the code being deployed work?

it's also crucial to ask

> Can I safely deploy this change given the currently running version of my
> service?

This second question is even more crucial in deployment environments where
**rolling update** deploys ensure the "old code" and the "new code" will need
to safely run side-by-side during every deploy.

Running database migrations is a **large** part of this equation. For example,
dropping a database column because the "new code" doesn't rely on it is not
safe because "old code" still relies on it. In simple situations like that,
it's crucial for operators to split the change into multiple stages:

-   Remove **code** that references the column
-   Deploy that code and ensure the deployed version is stable[ref]What do we
    mean by letting a deployment stabilize? Two things primarily: (1) the
    rolling update has completed so that the old code isn't running and
    (2) some form of acceptance testing to ensure the application doesn't need
    to rollback to a previous version[/ref]
-   Add a migration to drop the column
-   Run the migration and deploy the code again

### Making Migrations Safe for Rolling Updates {#making-safe}

With the motivation above, it's clear that **some** migrations just cannot be
run if it has been an extended period of time since the application was last
deployed. In order to provide some color, let's walk through a concrete use
case that must be done carefully to be safe in a rolling update deploy
environment.

We have a users table and want to add a **required** (i.e. `NOT NULL`) column
`display_name`:

```psql
golembic=> \d users
                         Table "public.users"
   Column   |          Type          | Collation | Nullable | Default
------------+------------------------+-----------+----------+---------
 id         | integer                |           | not null |
 email      | character varying(40)  |           |          |
 first_name | character varying(40)  |           | not null |
 last_name  | character varying(40)  |           | not null |
 city       | character varying(100) |           |          |
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "uq_users_email" UNIQUE, btree (email)
```

If we just add the column

```sql
ALTER TABLE
  users
ADD COLUMN
  display_name TEXT NOT NULL;
```

then the currently running code will fail on any inserts (since by definition
the code can't be inserting a `display_name` it never heard of):

```psql
golembic=> INSERT INTO
golembic->   users (id, email, first_name, last_name)
golembic-> VALUES
golembic->   (702188, 'dhermes@mail.invalid', 'Danny', 'Hermes');
ERROR:  null value in column "display_name" of relation "users" violates not-null constraint
DETAIL:  Failing row contains (702188, dhermes@mail.invalid, Danny, Hermes, null, null).
```

So we need to take a different approach. One way to add a **required** column
in a way that is safe for rolling updates would be to split it into two
migrations:

```sql
--- 986b93c5e494: Add the column, but allow it to be optional
ALTER TABLE
  users
ADD COLUMN
  display_name TEXT;
--- f37715e564e5: Backfill data into the column, then make the column required
UPDATE
  users
SET
  display_name = first_name || ' ' || last_name
WHERE
  display_name IS NULL;

ALTER TABLE
  users
ALTER COLUMN
  display_name
SET
  NOT NULL;
```

The application code can be updated to also write to the (optional)
`display_name` column and can be safely re-deployed after `986b93c5e494` runs.
Once that deploy has stabilized, the application code can be updated to
start to **read** and depend on the (required) `display_name` column and
can be safely re-deployed after `f37715e564e5` runs.

We call `986b93c5e494` a **milestone** migration because it is a special
inflection point in the revision history of the application. The migration
and the associated code must be deployed and stable **before** the next
migration (`f37715e564e5`) can run. In general, if multiple migrations are
introduced between two deploys, it's safe to apply all of them. However,
a **milestone** can only be run if it's the **last** migration being applied
in a sequence.

### Caveat {#caveat}

A milestone migration is in some sense a compromise. It mixes **purely**
database specific changes (migrations) with a proxy for the application
version. The proxy (is this milestone migration present in the codebase?)
gives an idication of where in the revision history the **application version**
is.

### Milestone Migration Tooling {#migration-tooling}

The `golembic` [library][1] directly provides support for marking a migration
as a milestone. Continuing with the `golembic` examples, we can commit
two separate changes to encode the migrations above:

#### Optional Column: `986b93c5e494` {#optional-column}

The first migration can specified as a milestone [in][2]
`examples/migrations.go`:

```go
[]golembic.MigrationOption{
	golembic.OptPrevious("432f690fcbda"),
	golembic.OptRevision("986b93c5e494"),
	golembic.OptMilestone(true),
	golembic.OptDescription("Add optional `users.display_name` column"),
	golembic.OptUpFromSQL("ALTER TABLE users ADD COLUMN display_name TEXT"),
},
```

#### Backfill and Require Column: `f37715e564e5` {#backfill-column}

Since the second migration requires (transactionally) running two migrations,
we introduce a function:

```go
const (
	backfillUsersDisplayName = `
UPDATE
  users
SET
  display_name = first_name || ' ' || last_name
WHERE
  display_name IS NULL
`
	requireUsersDisplayName = `
ALTER TABLE
  users
ALTER COLUMN
  display_name
SET
  NOT NULL
`
)

func RequiredDisplayName(ctx context.Context, tx *sql.Tx) error {
	_, err := tx.ExecContext(ctx, backfillUsersDisplayName)
	if err != nil {
		return err
	}

	_, err = tx.ExecContext(ctx, requireUsersDisplayName)
	return err
}
```

and then register this function in the migrations sequence:

```go
[]golembic.MigrationOption{
	golembic.OptPrevious("986b93c5e494"),
	golembic.OptRevision("f37715e564e5"),
	golembic.OptDescription("Backfill `users.display_name` column and make required"),
	golembic.OptUp(RequiredDisplayName),
},
```

### Guard Rails {#guard-rails}

If the next deploy targets the code after the second migration was merged,
the migrations tooling will refuse to run **any** of the migrations and
will cause a failure:

```text
$ make run-postgres-cmd GOLEMBIC_CMD=describe
...
6 | 432f690fcbda | Create movies table
7 | 986b93c5e494 | Add optional `users.display_name` column [MILESTONE]
8 | f37715e564e5 | Backfill `users.display_name` column and make required
$
$ make run-postgres-cmd
If a migration sequence contains a milestone, it must be the last migration; revision 986b93c5e494 (1 / 2 migrations)
exit status 1
make: *** [run-postgres-cmd] Error 1
```

This indicates that the service operator should back the truck up and deploy
an earlier version, i.e. one where only the first migration and the
associated code changes are present:

```text
$ make run-postgres-cmd GOLEMBIC_CMD=describe
...
6 | 432f690fcbda | Create movies table
7 | 986b93c5e494 | Add optional `users.display_name` column [MILESTONE]
$
$ make run-postgres-cmd
Applying 986b93c5e494: Add optional `users.display_name` column [MILESTONE]
```

After this **milestone** version stabilizes, the second migration can be run
and the associated code changes can be deployed:

```text
$ make run-postgres-cmd
Applying f37715e564e5: Backfill `users.display_name` column and make required
```

### Related {#related}

See [The Case for a Metadata Table for Database Migrations][3] for more context
on how metadata tables for migrations work.

<hr style="margin-bottom: 25px; width: 50%;">

[1]: https://github.com/dhermes/golembic/tree/2021.10.29
[2]: https://github.com/dhermes/golembic/blob/2021.10.29/examples/migrations.go#L69
[3]: /2021/10/database-migrations-table.html
