---
date: 2024-06-12
title: Almost unique (constraints)
description: Using PostgreSQL exclusion constraints when a UNIQUE doesn't fit
# author: Danny Hermes (dhermes@bossylobster.com)
# tags: PostgreSQL, SQL, database, constraint, TIL
# slug: almost-unique-constraint
# comments: true
# use_twitter_card: true
# use_open_graph: true
# use_schema_org: true
# twitter_site: @bossylobster
# twitter_creator: @bossylobster
# social_image: images/almost-unique.jpg
# github_slug: content/2024-06-12-almost-unique-constraint.md
---

<div markdown="1" style="text-align: center;">
  ![almost-unique](/images/almost-unique.jpg)
</div>

> It turns out it's quite straightforward to construct an "**almost** unique"
> constraint in PostgreSQL via `EXCLUDE`.

I was recently stuck in a jam in our PostgreSQL database during a feature
migration. We needed a "[partial][3] `UNIQUE`" constraint and I was surprised
to find out that PostgreSQL doesn't support them[ref]I was surprised because my
default assumption is that PostgreSQL can do [everything][4][/ref].

Luckily, a wild **TIL** appeared in a StackOverflow [answer][2] that pointed me
to [exclusion constraints][1]. It turns out it's quite straightforward to
construct an "**almost** unique" constraint in PostgreSQL via
`EXCLUDE`[ref]Read on if you'd like to know more, but the constraint presented
is the whole punchline![/ref]:

```sql
ALTER TABLE acme.event
  ADD CONSTRAINT uq_event_reference_id_event_type_slot_except_sentinel
  EXCLUDE USING GIST (reference_id WITH =, event_type WITH =, slot WITH =)
  WHERE (slot <> 0);
```

## Motivation

In the migration I referenced, we had a mature feature tracking events:

```sql
CREATE TABLE acme.event (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  reference_id UUID NOT NULL,
  event_type TEXT NOT NULL,
  slot INTEGER NOT NULL
);
```

For each entity (`reference_id`) and event type, the events are slotted in
the order that they are recorded[ref]And possibly swapped later by users[/ref].
The slot is required to be unique for a given entity and event type:

```sql
ALTER TABLE acme.event
  ADD CONSTRAINT uq_event_reference_id_event_type_slot
  UNIQUE (reference_id, event_type, slot);
```

In the migration in question, we wanted to enable events to be recorded before
the referenced entity was known. This would require allowing event inserts
without a reference ID and then later allowing events to be "promoted" by
assigning the reference ID (at which point a slot could be determined).

However, due to a **large** number of (non-nullable) uses of the `reference_id`
and `slot` columns in application code, we realized that we could do this
migration significantly faster if we introduced sentinel values for the
reference ID and the slot (`0`).

## What won't work

Now there's a problem: the `UNIQUE` index can't be enforced. It'll be overloaded
with rows containing sentinel values:

<!--
CREATE TABLE acme.reference (id UUID NOT NULL, ref_name TEXT NOT NULL);
INSERT INTO acme.reference (id, ref_name) VALUES ('aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a', 'sentinel');
INSERT INTO acme.event (id, reference_id, event_type, slot) VALUES ('32aa495d-84aa-456e-82f2-3ace6ed99286', 'aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a', 'boomerang', 0);
-->

```sql
SELECT ref_name FROM acme.reference WHERE id = 'aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a';
--  ref_name
-- ----------
--  sentinel
-- (1 row)
--

SELECT
  id, event_type, slot
FROM
  acme.event
WHERE
  reference_id = 'aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a';
--                   id                  | event_type | slot
-- --------------------------------------+------------+------
--  32aa495d-84aa-456e-82f2-3ace6ed99286 | boomerang  |    0
-- (1 row)
--

INSERT INTO
  acme.event (reference_id, event_type, slot)
VALUES
  ('aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a', 'boomerang', 0)
RETURNING id;
-- ERROR:  duplicate key value violates unique constraint "uq_event_reference_id_event_type_slot"
-- DETAIL:  Key (reference_id, event_type, slot)=(aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a, boomerang, 0) already exists.
```

I was expecting that partial `UNIQUE` constraints existed in the same way
[partial indexes do][3]. However I was mistaken:

```sql
ALTER TABLE acme.event
  DROP CONSTRAINT uq_event_reference_id_event_type_slot;
-- ALTER TABLE

----

ALTER TABLE acme.event
  ADD CONSTRAINT uq_event_reference_id_event_type_slot
  UNIQUE (reference_id, event_type, slot)
  WHERE (slot <> 0);
-- ERROR:  syntax error at or near "WHERE"
-- LINE 4:   WHERE (slot <> 0);
--           ^
```

## What will work

This where [exclusion constraints][1] come in! By using `EXCLUDE`, we can still
create a `CONSTRAINT` but also leave out the sentinel rows:

```sql
ALTER TABLE acme.event
  ADD CONSTRAINT uq_event_reference_id_event_type_slot_except_sentinel
  EXCLUDE USING GIST (reference_id WITH =, event_type WITH =, slot WITH =)
  WHERE (slot <> 0);
```

To understand the `WITH =` syntax, observe what happens if the exclusion
predicate `slot <> 0` is **NOT** satisfied. It functions exactly like a `UNIQUE`
constraint:

<!--
INSERT INTO
  acme.event (id, reference_id, event_type, slot)
VALUES
  ('a9b359c0-91ab-4d0f-8b16-1d08fca1923f', 'd3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3', 'frisbee', 1),
  ('8bbe2612-72d7-4397-93b4-08528be828f4', 'd3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3', 'frisbee', 2);
-->

```sql
SELECT
  id, event_type, slot
FROM
  acme.event
WHERE
  reference_id = 'd3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3';
--                   id                  | event_type | slot
-- --------------------------------------+------------+------
--  a9b359c0-91ab-4d0f-8b16-1d08fca1923f | frisbee    |    1
--  8bbe2612-72d7-4397-93b4-08528be828f4 | frisbee    |    2
-- (2 rows)
--

----

INSERT INTO
  acme.event (reference_id, event_type, slot)
VALUES
  ('d3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3', 'frisbee', 2)
RETURNING id;
-- ERROR:  conflicting key value violates exclusion constraint "uq_event_reference_id_event_type_slot_except_sentinel"
-- DETAIL:  Key (reference_id, event_type, slot)=(d3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3, frisbee, 2) conflicts with existing key (reference_id, event_type, slot)=(d3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3, frisbee, 2).

----

INSERT INTO
  acme.event (reference_id, event_type, slot)
VALUES
  ('d3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3', 'frisbee', 3)
RETURNING id;
--                   id
-- --------------------------------------
--  67a9d16c-5a97-47ce-a68f-eafaf4a9f56d
-- (1 row)
--
-- INSERT 0 1
```

On the other hand, the constraint **excludes** our sentinel rows and prevents
a conflict:

```sql
INSERT INTO
  acme.event (reference_id, event_type, slot)
VALUES
  ('aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a', 'boomerang', 0)
RETURNING id;
--                   id
-- --------------------------------------
--  1746f32b-8ce0-49c9-86ff-a28e2756021e
-- (1 row)
--
-- INSERT 0 1

----

SELECT
  id, event_type, slot
FROM
  acme.event
WHERE
  reference_id = 'aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a';
--                   id                  | event_type | slot
-- --------------------------------------+------------+------
--  32aa495d-84aa-456e-82f2-3ace6ed99286 | boomerang  |    0
--  1746f32b-8ce0-49c9-86ff-a28e2756021e | boomerang  |    0
-- (2 rows)
--
```

## Alternatives

As mentioned in a related StackOverflow [answer][5], a `UNIQUE INDEX` can be
used directly, in which case a partial index is still possible[ref]Since it's an
index and not a `UNIQUE` constraint[/ref]:

```sql
ALTER TABLE acme.event
  DROP CONSTRAINT uq_event_reference_id_event_type_slot_except_sentinel;
-- ALTER TABLE

----

CREATE UNIQUE INDEX ix_uq_event_reference_id_event_type_slot
  ON acme.event (reference_id, event_type, slot)
  WHERE (slot <> 0);
-- CREATE INDEX
```

This index functions exactly the same as the exclusion constraint:

```sql
INSERT INTO
  acme.event (reference_id, event_type, slot)
VALUES
  ('d3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3', 'frisbee', 2)
RETURNING id;
-- ERROR:  duplicate key value violates unique constraint "ix_uq_event_reference_id_event_type_slot"
-- DETAIL:  Key (reference_id, event_type, slot)=(d3521e28-9f1e-4fa4-b82d-bd5c33d0a0e3, frisbee, 2) already exists.

----

INSERT INTO
  acme.event (reference_id, event_type, slot)
VALUES
  ('aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a', 'boomerang', 0)
RETURNING id;
--                   id
-- --------------------------------------
--  192b2e4b-e11e-466d-af85-70cf27a1c7d8
-- (1 row)
--
-- INSERT 0 1

----

SELECT
  id, event_type, slot
FROM
  acme.event
WHERE
  reference_id = 'aa8a9ba8-7fc9-4b20-95bd-e8c3ff9c490a';
--                   id                  | event_type | slot
-- --------------------------------------+------------+------
--  32aa495d-84aa-456e-82f2-3ace6ed99286 | boomerang  |    0
--  1746f32b-8ce0-49c9-86ff-a28e2756021e | boomerang  |    0
--  192b2e4b-e11e-466d-af85-70cf27a1c7d8 | boomerang  |    0
-- (3 rows)
--
```

## Simpler wins!

In the end, we didn't need an exclusion constraint after all! We reexamined our
assumptions and realized that it'd be enough to just let the `reference_id` be
nullable while still using a sentinel slot value (`0`):

```diff
--- schema.before.sql  2024-06-12 13:37:00
+++ schema.after.sql   2024-06-12 13:37:00
@@ -1,6 +1,6 @@
 CREATE TABLE acme.event (
   id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
-  reference_id UUID NOT NULL,
+  reference_id UUID,
   event_type TEXT NOT NULL,
   slot INTEGER NOT NULL
 );
```

If **any** of the column values is `NULL`, the constraint doesn't apply, so
there would be no issues with duplicate slots:

```sql
ALTER TABLE acme.event
  ADD CONSTRAINT uq_event_reference_id_event_type_slot
  UNIQUE (reference_id, event_type, slot);
```

[1]: https://www.postgresql.org/docs/16/ddl-constraints.html#DDL-CONSTRAINTS-EXCLUSION
[2]: https://stackoverflow.com/a/48200472/1068170
[3]: https://www.postgresql.org/docs/16/indexes-partial.html
[4]: https://www.timescale.com/blog/how-to-collapse-your-stack-using-postgresql-for-everything/
[5]: https://stackoverflow.com/a/16236566/1068170
