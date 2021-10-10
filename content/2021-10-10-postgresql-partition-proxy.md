---
title: PostgreSQL Partition Proxy
description: Using a Foreign Data Wrapper for Routing to Shards
date: 2021-10-10
author: Danny Hermes (dhermes@bossylobster.com)
tags: PostgreSQL, Partition, Router, Sharding, Scaling, FDW
slug: postgresql-partition-proxy
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/db-router.png
github_slug: content/2021-10-10-postgresql-partition-proxy.md
---

<div markdown="1" style="text-align: center;">
  ![Database Router Proxy][102]
</div>

For most[ref]Most by application count, not weighted by amount of
data.[/ref] application databases, the problem of horizontally scaling the
database into distinct physical shards will **never** need to be solved.
This is bliss! However, some teams lucky enough to hit scale are also unlucky
enough to hit the limits of [vertical scaling][108]. If you don't need to
partition, please don't do it prematurely (or ever) just because this post
sounds cool.

There are **many** ways to approach the partitioning problem and we won't
explore that space in full here. I recommend a recent [post][101] from Notion
for some of the finer points[ref]For example, the term "shard" is believed
to originate from a database backing an MMORPG.[/ref]. The goal of this
post is to explore a PostgreSQL-native approach that handles **routing**
requests to the correct physical shard where a logical shard resides.

### Contents

-   [Prerequisities](#prerequisities)
-   [Mechanics](#mechanics)
-   [The Router](#the-router)

### Prerequisities {#prerequisities}

In order to set the stage, let's define a few terms and lay out the approach
we'll take here at a high level.

-   **Vertical Scaling**: Increasing attributes of a database instance to
    improve performance, such as memory, disk and networking hardware.
-   **Horizontal Scaling**: Adding more database instances to a database
    cluster to distribute the work.
-   **Partition**: The act of splitting a database into distinct pieces; this
    is usually done when database usage exceeds the limits of a single
    instance.
-   **Logical Shard**: A subset of application data sharing a common attribute,
    typically referred to as a shard key or partition key. For example in a
    multitenant application the partition key may just be the tenant or
    customer identifier.
-   **Physical Shard**: One (of many) physical database instances where
    application data resides. It's common for multiple logical shards to
    reside on the same physical shard, but not always.
-   **Proxy**: An intermediary between a client (here, a backend application)
    and a server (here, a database). Often a proxy provides extra features
    that the server does not have, like DDOS protection, secure connections
    via TLS or load balancing.
-   **Database Router**: A proxy that is configured to dispatch queries
    to the correct physical shard based on the requested logical shard.

Below we explore how we can use a veneer[ref]Here "veneer" just means the
instance if superficial, i.e. doesn't contain any real data.[/ref] PostgreSQL
instance as a proxy router into each physical shard.

### Mechanics {#mechanics}

In the "before times", an application can be configured to reach **the**
database with connection parameters for a single database server. After
the application database has been physically partitioned, it is no longer so
simple. One choice here is to just manage the increased complexity in the
application[ref]This is mentioned in the Notion [post][101].[/ref]. This
has a few downsides:

-   If a logical shard is **moved**, the application will need to update
    configuration on the fly[ref]The stale configuration problem can mostly be
    addressed by loading configuration from a database (vs. hardcoding it in
    source code) and using triggers (e.g. configuration file `mtime` or
    sending a `SIGHUP`) to reload configuration without a restart or
    redeploy.[/ref]
-   The application will need `P` connection pools &mdash; one for each
    physical shard
-   The boundary between database and application is now blurred; the
    application has now taken on a nontrivial amount of the complexity that
    was previously reserved for the database

Instead of pushing this shard bookkeeping responsibility into the application,
we rely on a veneer PostgreSQL instance as a proxy router. By using a router,
the application can blissfully continue to use configuration for a single
database server (now the router instead of the original database instance).

There are many[ref]I have explicitly left out using [row level security][110]
as a partitioning strategy here because it requires an implicit partition key,
which is more challenging for a physical partition than an explicit partition
key.[/ref] choices here for **how** to do the physical partitioning, including

-   Native [table partitions][109] for each logical shard
-   Separate `DATABASE` for each logical shard
-   Separate `SCHEMA` ([docs][111]) for each logical shard

For this post, we'll be choosing a distinct schema for each logical shard and
will assume the schema name is the partition key. The native table partitions
are a bit more of a challenge with a physically partitioned database cluster.
The shard-by-`DATABASE` approach requires `L` connection pools &mdash; one
for each **logical** shard, due to the way the PostgreSQL wire protocol works
(a connection is to a `DATABASE`, not to a PostgreSQL instance).

Though using the proxy router eliminates some code and operational complexity
in the application, it's not all bliss! Even before the physical partition
happens, the application code will likely require updating **every query**
to include the schema name and operationally, many database migrations will be
needed to move data into the newly created schemas.

### The Router {#the-router}

Some database ecosystems already have commonly used routers, for example
the `mongos` [router][106] in the MongoDB ecosystem. We use `mongos`
[at Blend][107] in a textbook multitenant system, but there is no equivalent
to reach for in the PostgreSQL ecosystem.

Writing a proxy is not easy, it requires deep knowledge of the networking stack
(usually TCP). Proxy code must be highly concurrent and performant to avoid
adding overhead to proxied traffic. Adding to the degree of difficulty here,
our database proxy needs to support the PostgreSQL wire protocol and would
likely need to parse queries on the fly to do routing.

Implementing a router from scratch with these requirements sounds like a fun
side project to some. Deploying that side project into production for a
database used by real customers sounds like a nightmare. This is where
PostgreSQL comes to the rescue! Kirk Roybal [said][105] it best

> You want to extract data from other systems? PostgreSQL has the most vibrant
> collection of federation objects of any database. They call them foreign data
> wrappers, and you can hook PostgreSQL to an alligator with duct tape and zip
> ties. Treat anything like it's your data.

The concept of a foreign data wrapper (FDW) was added to PostgreSQL in 2013.
Arguably the highest quality FDW in the entire PostgreSQL ecosystem is the
native one: `postgres_fdw`. The `postgres_fdw` extension ships with stock
PostgreSQL[ref]The `postgres_fdw` extension is also [supported][112] on
RDS.[/ref] and allows federating queries to a "foreign table" resident on
another PostgreSQL instance.

### Show Me {#show-me}

I made an entire GitHub [repository][104] to spin up a test rig locally.
Let's dig into the mechanics of how the router (`veneer`) is set up, how
it connects to each physical shard and how a query makes it to one of the
schemas containing a logical shard. For our local testing we have:

-   Router PostgreSQL instance running in `dev-postgres-veneer` Docker
    container
-   Three physical PostgreSQL shards running in `dev-postgres-shard{1,2,3}`
    Docker containers
-   Application roles `veneer_app` in the router and `bookstore_app` in
    each shard
-   Admin role roles `veneer_admin` in the router and `bookstore_admin` in
    each shard for performing migrations
-   Four schemas `bluth_co` (shard 1), `cyberdyne` (shard 2),
    `dunder_mifflin` (shard 2) and `initech` (shard 3)
-   Two partitioned tables `authors` and `books` present in each schema

To configure a single shard, we create a FDW server in `veneer`:

```sql
CREATE SERVER shard2_server
  FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'dev-postgres-shard2.', port '5432', dbname 'bookstore');
```

and then provide mappings for our `veneer` application and admin users into
the FDW server equivalents:

```sql
CREATE USER MAPPING FOR veneer_admin
  SERVER shard2_server
  OPTIONS (user 'bookstore_admin', password 'ijkl9012');
CREATE USER MAPPING FOR veneer_app
  SERVER shard2_server
  OPTIONS (user 'bookstore_app', password '9012ijkl');
```

Finally, we import all tables from each logical schema[ref]There is a lot more
to say about importing foreign tables, particularly around migrations and
application lifecycle. I'll try to write about it soon.[/ref]:

```sql
IMPORT FOREIGN SCHEMA cyberdyne
  FROM SERVER shard2_server
  INTO cyberdyne;
IMPORT FOREIGN SCHEMA dunder_mifflin
  FROM SERVER shard2_server
  INTO dunder_mifflin;
```

For example a table on `dev-postgres-shard2`:

```sql
bookstore=> \d+ cyberdyne.authors
                                 Table "cyberdyne.authors"
   Column   | Type | Collation | Nullable | Default | Storage  | Stats target | Description
------------+------+-----------+----------+---------+----------+--------------+-------------
 id         | uuid |           | not null |         | plain    |              |
 first_name | text |           | not null |         | extended |              |
 last_name  | text |           | not null |         | extended |              |
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
    "uq_authors_full_name" UNIQUE CONSTRAINT, btree (first_name, last_name)
Referenced by:
    TABLE "cyberdyne.books" CONSTRAINT "books_author_id_fkey" FOREIGN KEY (author_id) REFERENCES cyberdyne.authors(id)
Access method: heap
```

gets imported as

```sql
veneer=> \d+ cyberdyne.authors
                                            Foreign table "cyberdyne.authors"
   Column   | Type | Collation | Nullable | Default |        FDW options         | Storage  | Stats target | Description
------------+------+-----------+----------+---------+----------------------------+----------+--------------+-------------
 id         | uuid |           | not null |         | (column_name 'id')         | plain    |              |
 first_name | text |           | not null |         | (column_name 'first_name') | extended |              |
 last_name  | text |           | not null |         | (column_name 'last_name')  | extended |              |
Server: shard2_server
FDW options: (schema_name 'cyberdyne', table_name 'authors')
```

Running a query from `veneer` proxies even complex queries within the
same partition key (schema) to the correct physical shard:

```sql
veneer=> SELECT
veneer->   a.id AS author_id,
veneer->   b.id AS book_id,
veneer->   a.first_name AS author_first_name,
veneer->   a.last_name AS author_last_name,
veneer->   b.title AS title,
veneer->   b.publish_date AS publish_date
veneer-> FROM
veneer->   bluth_co.authors AS a
veneer-> INNER JOIN
veneer->   bluth_co.books AS b
veneer-> ON
veneer->   a.id = b.author_id
veneer-> WHERE
veneer->   a.last_name = 'Rice';
              author_id               |               book_id                | author_first_name | author_last_name |           title            | publish_date
--------------------------------------+--------------------------------------+-------------------+------------------+----------------------------+--------------
 54b44bc0-fb42-4937-a5f9-9be5a1bcb844 | 97f2477b-cd10-4474-8899-e19c07270f13 | Anne              | Rice             | The Wolf Gift              | 2012-02-14
 54b44bc0-fb42-4937-a5f9-9be5a1bcb844 | b2d43d29-3a64-4c0d-8741-db8c103db7ee | Anne              | Rice             | Interview with the Vampire | 1976-05-05
 54b44bc0-fb42-4937-a5f9-9be5a1bcb844 | 3537896e-47cc-4bda-a348-a11a56430d8a | Anne              | Rice             | The Queen of the Damned    | 1988-09-12
(3 rows)
```

<div markdown="1" style="text-align: center;">
  ![PostgreSQL][103]
</div>

<hr style="margin-bottom: 25px; width: 50%;">

[108]: https://pgdash.io/blog/scaling-postgres.html
[101]: https://www.notion.so/blog/sharding-postgres-at-notion
[109]: https://www.postgresql.org/docs/14/ddl-partitioning.html
[110]: https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/
[111]: https://www.postgresql.org/docs/14/ddl-schemas.html
[112]: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts.General.FeatureSupport.Extensions.13x
[106]: https://docs.mongodb.com/manual/core/sharded-cluster-query-router/
[107]: https://full-stack.blend.com/scaling-mongodb-for-a-growing-customer-base.html
[105]: https://www.2ndquadrant.com/en/blog/postgresql-is-the-worlds-best-database/
[104]: https://github.com/dhermes/postgresql-partition-proxy/tree/2021.10.10

[102]: /images/db-router.png
[103]: /images/postgresql-elephant.svg
