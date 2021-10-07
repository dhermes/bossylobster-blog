---
title: Go Duration, PostgreSQL Interval
description: Best of Both Worlds
date: 2021-10-06
author: Danny Hermes (dhermes@bossylobster.com)
tags: Go, Golang, PostgreSQL, Time, Duration, Interval
slug: go-duration-postgresql-interval
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/TODO.png
github_slug: content/2021-10-06-go-duration-postgresql-interval.md
---

Building a web application in Go and using PostgreSQL as the database is a real
joy. Both of these tools are produced by incredibly vibrant open source
projects. These projects represent some of the best attributes of the open
source movement. When used in combination, occasionally idioms from Go don't
translate to PostgreSQL and vice versa. Often this can be chalked up to the
object-relational impedance [mismatch][1], but not always[ref]Since a core
design goal of Go is composition over inheritance, typical OOP patterns aren't
that prevalant. As a result, object-relational impedance mismatch doesn't
really rear its head very often.[/ref].

Recently, a [teammate][2] and I bumped up against one of these rare situations
where the idioms don't line up. In Go, `time.Duration` is an integer, but
in PostgreSQL `INTERVAL` is essentially text from an application's perspective.

### Go Details {#go-details}

The `time.Duration` standard library [type][3] is a 64-bit integer, with
associated methods tacked on via a type definition declaration:

```go
type Duration int64
```

This type can represent durations accurate to nanosecond precision, with
positive and negative extremes around 292 years.

### PostgreSQL Details {#postgresql-details}

The PostgreSQL `INTERVAL` type is [stored][4] as 128-bits internally and is
serialized as text over the wire in one of four [output][5] formats.
It has less precision than a Go `time.Duration` (microseconds instead of
nanoseconds) but due to having twice as much space for storage, can support
much larger magnitudes: positive and negative extremes around 178,000,000
years.

### Now What? {#now-what}

TL;DR using Go and PostgreSQL idioms simultaneously is beneficial, let's try
to make it work.

If the types are **so** different, what can we do? First of all, it's important
to understand the use case. The **overwhelming** majority of applications
are just fine with the lowest common denominator covered by both types:
microsecond precision and positive and negative extremes around 292 years.
For applications outside this majority, this is where you give up and roll
your own.

But even with this, why not just use a `string` in Go or use a `BIGINT` in
PostgreSQL[ref]A PostgreSQL `BIGINT` exactly maps to `int64` in Go.[/ref]? A
`string` in Go would be pretty worthless for actual use beyond just telling
the database to do **all** of the business logic involving intervals. Using a
`BIGINT` in PostgreSQL similarly limits hinders the database. For example, an
`INTERVAL` allows sweeping for stale sessions in a PostgreSQL native way:

```sql
-- CREATE TABLE web_sessions (
--   id UUID NOT NULL,
--   email TEXT NOT NULL,
--   created_at TIMESTAMP WITH TIME ZONE NOT NULL,
--   updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
--   max_age INTERVAL
-- )
SELECT
  id, email
FROM
  web_sessions
WHERE
  updated_at < (NOW() - max_age)
```

Conversion from `BIGINT` **to** `INTERVAL` can be done on the fly but this
breaks down for certain inputs:

```sql
go_duration=> SELECT EXTRACT(epoch from '3 days 04:05:06'::INTERVAL);
 date_part
-----------
    273906
(1 row)

go_duration=> SELECT make_interval(secs => 273906);
 make_interval
---------------
 76:05:06
(1 row)

go_duration=> SELECT
go_duration->   make_interval(days => 3, hours => 4, mins => 5, secs => 6) -
go_duration->   make_interval(secs => 273906) AS delta;
      delta
------------------
 3 days -72:00:00
(1 row)
```

### Making Go Do the Work {#making-go-do-the-work}

In cases like this &mdash; where the database wire representation differs from
the target value in Go &mdash; the Go standard library has our back. The
`sql.Scanner` [interface][6] allows custom transformation when reading data
in and the `driver.Valuer` [interface][7] allows custom transformation when
writing data out.

For example, assuming the active PostgreSQL session has `IntervalStyle` set
to `postgres`:

```go
type DurationWrapped struct {
	time.Duration
}

func (dw *DurationWrapped) Scan(src interface{}) error {
	if src == nil {
		dw.Duration = 0
		return nil
	}

	srcStr, ok := src.(string)
  if !ok {
		return fmt.Errorf("duration column was not text; type %T", src)
	}

	// See: https://www.postgresql.org/docs/14/datatype-datetime.html
	//      IntervalStyle Output Table
	return unmarshalForIntervalStyle(srcStr, "postgres", &dw.Duration)
}

func (dw DurationWrapped) Value() (driver.Value, error) {
	return marshalForIntervalStyle(dw.Duration, "postgres"), nil
}
```

This approach works great in codebases where database calls directly interact
with `database/sql` primitives:

```go
_, err = pool.ExecContext(ctx, "UPDATE ... max_age = $1", dw)
// ...
rows, err := pool.QueryContext(ctx, "SELECT ...")
// ...
err = rows.Scan(&session.ID, &session.Email, &session.UpdatedAt, &dw)
session.MaxAge = dw.Duration
```

However, it's common for Go codebases to use a higher-level ORM or database
package that uses reflection to map database columns to fields in a Go struct.
For such codebases, it may be much more challenging (or even impossible) to
use a `DurationWrapped` value. It would be possible to just use a
`DurationWrapped` as the column type:

```go
type Session struct {
	ID        uuid.UUID       `db:"id"`
	Email     string          `db:"email"`
	CreatedAt time.Time       `db:"created_at"`
	UpdatedAt time.Time       `db:"updated_at"`
	MaxAge    DurationWrapped `db:"max_age"`
}
```

However, using a `DurationWrapped` instead of a `time.Duration` **everywhere**
the type is used is a large sacrifice. In my opinion, it is the tail wagging
the dog.

### Making PostgreSQL Do the Work {#making-postgresql-do-the-work}

Instead of doing all the work in Go, we could instead invert the approach and
do all of the extra work in PostgreSQL. It's likely that most of this
conversion work will be more efficient (and possibly more correct) when done
in PostgreSQL vs. in our application code.

For example, when **reading**, convert to nanoseconds in the
database[ref]The `::BIGINT` conversion can go poorly for `INTERVAL` values
that produce an epoch value too large to fit in an `int64`, but we are assuming
our application doesn't need such values.[/ref]:

```sql
SELECT
  id, email, (EXTRACT(epoch FROM max_age) * 1000000000)::BIGINT
FROM
  web_sessions
```

and when **writing**, make a best effort to convert from nanoseconds to
an `INTERVAL`:

```sql
-- -- NOTE: This is likely too simple.
-- CREATE OR REPLACE FUNCTION interval_from_nanoseconds(ns BIGINT)
-- RETURNS INTERVAL AS $$
-- SELECT make_interval(secs => ns::NUMERIC / 1000000000);
-- $$ LANGUAGE sql;
UPDATE web_sessions
SET
  updated_at = NOW(),
  max_age = interval_from_nanoseconds($2)
WHERE
  id = $1
```

### Takeaways {#takeaways}

Clearly, the above approaches are filled with sharp corners and compromise.
However, the compromises above are likely acceptable for most applications
and the have the **huge** benefit of allowing usage of the Go and PostgreSQL
types that are "standard" for the task at hand.

The `time.Duration` and `INTERVAL` types are fundamentally designed for
different purposes &mdash; e.g. `'1 year 2 mons'::INTERVAL` always means "add a
year and a month" independent of the literal number of nanoseconds between the
two timestamps. In order to benefit from both of them, it's important to ensure
that usage both in Go and PostgreSQL aligns with the common set of
functionality shared by both types.

<hr style="margin-bottom: 25px; width: 50%;">

[1]: https://en.wikipedia.org/wiki/Object%E2%80%93relational_impedance_mismatch
[2]: https://twitter.com/perryfromsoma
[3]: https://github.com/golang/go/blob/go1.17.1/src/time/time.go#L587-L590
[4]: https://www.postgresql.org/docs/14/datatype-datetime.html
[5]: https://www.postgresql.org/docs/14/datatype-datetime.html#INTERVAL-STYLE-OUTPUT-TABLE
[6]: https://github.com/golang/go/blob/go1.17.1/src/database/sql/sql.go#L395-L416
[7]: https://github.com/golang/go/blob/go1.17.1/src/database/sql/driver/types.go#L35-L43
