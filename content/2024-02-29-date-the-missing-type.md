---
title: "The missing type in the Go standard library: Date!"
description: Introducing the go-date package. Filling in the gap left by the Go standard library.
date: 2024-02-29
author: Danny Hermes (dhermes@bossylobster.com)
tags: Go, Date, Datetime, Standard library
slug: date-the-missing-type
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/calendar-pins.jpg
github_slug: content/2024-02-29-date-the-missing-type.md
---

<div markdown="1" style="text-align: center;">
  ![go-date](/images/calendar-pins.jpg)
</div>

The Go standard library uses a single overloaded [type][1] as a stand-in for
both full datetimes[ref]Here by **datetime**, we mean an object that contains
**both** date (year, month, day), time information (hour, minute, second,
millisecond / microsecond / nanosecond), and often a relevant timezone as well.
For example this is provided by the `datetime.datetime` [type][4] in Python and
`Date` in JavaScript.[/ref] and dates. This mostly "just works", but slowly
starts to **degrade correctness** in codebases where both datetime and date
values need to [interact][2].

We store events using a mix of datetime and date [columns][8] in our database
(depending on the type of event). Having a mix of datetimes and date values
became a persistent source of subtle confusion and extended discussion[ref]Those
discussions usually included a phrase like "I wish the Go standard library had a
separate `Date` type"![/ref] within our engineering team. As a result, we
created a simple `Date` type that organically grew until it could replace all of
our existing usage of `time.Time`.

The `go-date` [package][3] is here to fill the gap left by the Go standard
library!

> Having a mix of datetimes and date values became a persistent source of subtle
> confusion and extended discussion within our engineering team

## Opportunity for correctness to degrade

To understand an example where correctness can start to degrade, consider
a datetime value (`now`) and a date value (`deadline`):

```go
now := time.Now()
// Common convention for date values is to use a `time.Time` with
// only the year, month, and day set. For example, this convention
// is followed by the standard library when a timestamp of the form
// YYYY-MM-DD is parsed via `time.Parse(time.DateOnly, value)`.
deadline := time.Date(2024, time.March, 1, 0, 0, 0, 0, time.UTC)
```

With two `time.Time` values, it's very reasonable for a developer to
compute the check "current date is on or before the deadline" via:

```go
withinDeadline := !now.After(deadline)
```

However, this is problematic for at least two reasons. First and foremost, the
timestamp of `deadline` is `00:00`, so it leaves out virtually 100% of the
deadline day. Secondly, the concept of "today" depends[ref]Why does the "today"
depend on the timezone? If a friend from Los Angeles calls at 11pm, but you're
in New York, today is tomorrow! (Or yesterday, depending on who says it.)[/ref]
on the **timezone** and for many applications, the application user likely has a
specific timezone that is natural for that check.

In codebases maintained over time by teams of different people, it's very
common for a developer to come in and edit existing code that they didn't
write. In cases like this, it's easy to have less context than the original
author.

Without sufficient context, mixing up the precision of `now` (datetime) and the
precision of `deadline` (date) is an easy mistake to make. On the other hand, if
`deadline` was not the same type as `now`, developers are forced to consider the
difference between the two types and account for this difference. If a `Date`
was used to represent the deadline instead:

```go
deadlineDate := date.NewDate(2024, time.March, 1)
```

then a correct implementation can both incorporate the timezone and ensure
that same percentage of the hours in the day are not erroneously ignored:

```go
nowDate := date.InTimezone(now, tz)
withinDeadline := !nowDate.After(deadlineDate)
```

<div markdown="1" style="text-align: center;">
  ![Missing pieces](/images/puzzle-missing-pieces.jpg)
</div>

## Integrating with sqlc

We use the `sqlc` [library][6] at Hardfin for all Go code that interacts with
the database. (See the wonderful [post][5] by PostgreSQL blogging legend Brandur
Leach for some of the benefits of `sqlc`.)

Out of the box, `sqlc` uses a Go `time.Time` both for columns of type
`TIMESTAMPTZ` and `DATE`. When reading `DATE` values (which come over the
wire in the form YYYY-MM-DD), the Go standard library produces values of the
form:

```go
time.Date(YYYY, MM, DD, 0, 0, 0, 0, time.UTC)
```

Instead, we can instruct `sqlc` to **globally** use `date.Date` and
`date.NullDate` when parsing `DATE` columns:

```yaml
---
version: "2"
overrides:
  go:
    overrides:
      - go_type:
          import: github.com/hardfinhq/go-date
          package: date
          type: NullDate
        db_type: date
        nullable: true
      - go_type:
          import: github.com/hardfinhq/go-date
          package: date
          type: Date
        db_type: date
        nullable: false
```

## Why do _we_ care?

At Hardfin, we help equipment manufacturers automate their financial operations
by connecting real world **events** to hardware subscriptions. This inherently
means we collect and store **a lot** of dates.

For many event types, we are able to collect both the date and the timestamp.
For example, if a user action occurs in our application or if an update comes in
from a third party system like Stripe. However for some events, the timestamp is
not required, not important, and oftentimes not known. For example, an operator
may know that "a robot was shipped on December 28" but may not know the exact
time of day that robot was shipped. The date December 28 has enough information
**without the timestamp** to trigger automation for the manufacturer's billing
and revenue.

<div markdown="1" style="text-align: center;">
  ![Connecting events](/images/train-aerial-view.jpg)
</div>

## Go forth and differentiate

This package is intended to be **simple**! (Simple to understand and simple to
implement.) The package is only intended to cover "modern" dates (i.e. dates
between the years 1900 and 2100) and so it can avoid resorting to the
[proleptic Gregorian calendar][7].

As a result, the core `Date` type directly exposes the year, month, and day as
struct fields.

We hope this package will come in handy for teams that need to draw a clear
distinction between datetime and date values!

<div markdown="1" style="text-align: center;">
  ![Pick a date](/images/calendar-clipboard.jpg)
</div>

[1]: https://pkg.go.dev/time#Time
[2]: #opportunity-for-correctness-to-degrade
[3]: https://pkg.go.dev/github.com/hardfinhq/go-date
[4]: https://docs.python.org/3/library/datetime.html
[5]: https://brandur.org/sqlc
[6]: https://docs.sqlc.dev
[7]: https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar
[8]: https://www.postgresql.org/docs/16/datatype-datetime.html
