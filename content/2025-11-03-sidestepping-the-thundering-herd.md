---
title: Sidestepping the Thundering Herd
description: Data pipelines for aggressively caching expensive SQL
date: 2025-11-03
author: Danny Hermes (dhermes@bossylobster.com)
tags: SQL, Cloud architecture, Data pipeline, Cloud Storage, JSON
slug: sidestepping-the-thundering-herd
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/thundering-herd.jpg
github_slug: content/2025-11-03-sidestepping-the-thundering-herd.md
---

<div markdown="1" style="text-align: center;">
  ![thundering-herd](/images/thundering-herd.jpg)
</div>

> This is cross-posted from the WorkWhile engineering [blog][7].

This post describes a data pipeline we built to convert an analytical SQL query
into an aggressively cached JSON API with zero load on our database or
application.

### Contents

- [Motivation](#motivation)
- [Core problem](#core-problem)
- [Cloud primitives for the win](#cloud-primitives)
- [Conclusion](#conclusion)

### Motivation {#motivation}

WorkWhile is the [labor marketplace of the future][6]. Our Econ Lab is on a
mission to harness the large corpus of data generated on our labor platform to
create new insights about the state of this emerging economy as well as the
overall U.S. economy. As part of this mission to unlock insights, we recently
[launched][1] a new economic index [ALUR][2] that measures labor force
utilization[ref]A close proxy (and _potentially_ more precise, depending on who
you ask) measure of national unemployment[/ref] and a group of economic
indicators [RISE][3] that measure directional trends in wage data.

As part of socializing these new economic metrics, we went all out and showcased
them on billboards from Times Square to San Francisco's financial district to
the Las Vegas strip. With that level of visibility, we'd need to serve these
metrics **a lot** and maintain a real-time feed to track any changes to these
over time.

### Core problem {#core-problem}

<div markdown="1" style="text-align: center;">
  ![traffic-jam](/images/traffic-jam.jpg)
</div>

These time series help provide insight on a daily or monthly basis into
ever-changing economic conditions. Computing and aggregating these values
requires significant work from our database, but it's work that is largely
static. In particular, "past" data is unlikely to **ever** change, and "current"
data (i.e. current day and preceding few days) is only being updated marginally.

Querying the production database[ref]Primary **or** replica, still too much
load![/ref] directly would result in high latency and heavy load due to repeated
execution of an expensive query. While these metrics originate from our core
application data, this isn't a user-facing feature[ref]Our users are workers and
employers (not economists)[/ref]; it's a data product. That's why we chose not
to serve this request **AT ALL** from our primary application infrastructure.

### Cloud primitives for the win {#cloud-primitives}

<div markdown="1" style="text-align: center;">
  ![data-pipeline](/images/thundering-herd-data-pipeline.jpg)
</div>

Luckily, we have several core tools to help us build a data product exactly
tailored to our needs. Rather than pursue extreme measures to make this work
within our existing API, we were able to easily build a data pipeline that
removed almost all operational burden.

- **Use a `MATERIALIZED VIEW` in our PostgreSQL database**: this allows us to
  pay the cost of running the expensive SQL query once, but as close to the
  data as possible (i.e. directly in the DB).
- **Periodic export to Cloud Storage**: as the economic metrics are updated
  throughout the day, we query the `MATERIALIZED VIEW` and create a JSON
  response that we can serve via Cloud Storage to power frontends that
  visualize the data.
- **CDN for caching**: once the data is in a Google Cloud Storage bucket, we
  front it with a Google Cloud Load Balancer that provides CDN functionality.
  This way the data can be loaded again and again with zero load on **ANY**
  of our infrastructure.

What's more, we were able to specify 100% of this **infrastructure as code**
with [Terraform][5]. This immediately paid dividends when we expanded from one
index (ALUR) to many (RISE) because we were able to re-use all of the same
primitives without having to revisit any of the decisions.

### Conclusion {#conclusion}

I spent approximately one full day turning this over in my mind trying to figure
out how we could avoid accidentally taking down production to make this work.
The breakthrough came from one phrase from the inimitable
[Matt Blair][4][ref]While I was walking in the park on a sunny day, a great
place to have a light bulb moment![/ref]:

> We need something to just cache the heck out of this

Once I heard that, my mind instantly went to CDN, and the last piece of the
puzzle was in place!

When architecture and tooling are well-considered, tasks like this become
simple, freeing operations teams from unnecessary stress. By utilizing cloud
primitives, we didn't need to run a new service, reinvent caching strategies, or
go deep in any other direction. By using the `MATERIALIZED VIEW`, we avoided
having to worry about spinning up a new system for dealing with data outside of
the application (e.g., a data lake) and the problems that would come with it
(e.g., production hardening, observability, etc.)

This is absolutely a case of _work smarter, not harder_!

[1]: https://www.workwhile.ai/blog/before-the-print-using-alur-to-nowcast-u-s-labor-force-data
[2]: https://www.workwhile.ai/alur
[3]: https://www.workwhile.ai/rise
[4]: https://www.linkedin.com/in/mattblair/
[5]: https://developer.hashicorp.com/terraform
[6]: https://www.workwhile.ai/blog/fractional-labor-the-united-states-untapped-workforce
[7]: https://tech.workwhile.ai/blog/sidestepping-the-thundering-herd-h6ndtck9
