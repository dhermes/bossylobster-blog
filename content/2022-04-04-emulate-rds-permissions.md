---
title: Emulating RDS Permissions with Terraform
description: Keeping local development in lock-step with RDS. Avoiding costly mistakes like locking out the RDS master user.
date: 2022-04-04
author: Danny Hermes (dhermes@bossylobster.com)
tags: Terraform, Docker, PostgreSQL
slug: emulate-rds-permissions
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/terraform-postgresql-and-rds.png
github_slug: content/2022-04-04-emulate-rds-permissions.md
---

<div markdown="1" style="text-align: center;">
  ![Terraform, PostgreSQL and RDS](/images/terraform-postgresql-and-rds.png)
</div>

> This is cross-posted from the Hardfin engineering [blog][6].

At Hardfin, we use AWS RDS for managed PostgreSQL instances to simplify our
infrastructure and focus on product. For the most part, RDS is
"just PostgreSQL" and acts like the PostgreSQL instances that we run on our
development machines. Unfortunately, it differs in a few key ways &mdash;
and that opens the door for dreaded "it works on my machine" issues.

We recently encountered a surprising error in RDS, which we couldn't replicate
in our local development setup. In order to prevent future issues like
this, we took steps to make our Dockerized PostgreSQL instance much more
similar to an RDS instance.

We are big proponents of Infrastructure-as-Code at Hardfin. We utilize
[Terraform][1] to describe as much of our infrastructure as we can, including
AWS RDS instances running PostgreSQL.

In addition to AWS resources, we use Terraform to directly manage some
PostgreSQL resources. A fresh RDS instance comes with a single role (the RDS
master user) available to DB operators. We **only** use this this RDS master
user via the [PostgreSQL provider][2] to create new application roles with
minimal privileges.

## Getting locked out

RDS [best practices][3] recommend against using the RDS master user within
applications; it has elevated privileges beyond what applications should be able
to do.

As part of scoping a minimal set of privileges, we utilize grants to create
(1) an admin role used during migrations and other offline operations, and,
(2) an application role used directly while running the application. The admin
role permissions allow a full set of [DDL][4] operations while the application
role has a scope limited to [DML][5] operations.

As part of the process of limiting access, we merged a change to limit which
roles can `CONNECT` to a PostgreSQL `DATABASE` and to even further limit which
roles can `CREATE` in the `DATABASE`. After running this against a Dockerized
PostgreSQL instance used for local development, all changes were applied
successfully.

Once unit tests passed in CI, we merged the change and ran the Terraform plan in
our `sandbox` environment against an actual RDS instance. These changes too were
applied successfully, or so we thought. Later that day, another small change was
made to the same Terraform workspace. With no signs of trouble in testing, this
change was merged. When we went to generate a plan in `sandbox`, we found out
the RDS master user was **locked out**:

```bash
$ terraform apply
...
postgresql_grant.revoke_public: Refreshing state... [id=public_initech_database]
...
╷
│ Error: error detecting capabilities: error PostgreSQL version: pq: permission denied for database "initech"
│
│   with postgresql_grant.revoke_public,
│   on grants.tf line 6, in resource "postgresql_grant" "revoke_public":
│    6: resource "postgresql_grant" "revoke_public" {
│
╵
...
```

## What went wrong

The RDS master user got locked out as a result of a change that introduced
three `DATABASE` grants:

```hcl
resource "postgresql_grant" "revoke_public" {
  database    = postgresql_database.initech.name
  role        = "public"
  object_type = "database"
  privileges  = []
}

resource "postgresql_grant" "app_role_connect" {
  database    = postgresql_database.initech.name
  role        = postgresql_role.app_role_gibbons.name
  object_type = "database"
  privileges  = ["CONNECT"]
}

resource "postgresql_grant" "admin_role_full" {
  database    = postgresql_database.initech.name
  role        = postgresql_role.admin_role_lumbergh.name
  object_type = "database"
  privileges  = ["CREATE", "TEMPORARY", "CONNECT"]
}
```

After applying, only the admin and application role were allowed to connect
to the database[ref]The `DATABASE` privileges (e.g. `lumbergh=CTc/lumbergh+`)
corresponds to CREATE (`C`), TEMPORARY (`T`) and CONNECT (`c`).[/ref]:

```sql
initech=> \l initech
                                 List of databases
  Name   |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
---------+----------+----------+-------------+-------------+-----------------------
 initech | lumbergh | UTF8     | en_US.UTF-8 | en_US.UTF-8 | lumbergh=CTc/lumbergh+
         |          |          |             |             | gibbons=c/lumbergh
(1 row)
```

Crucially, this list does not include the RDS master user:

```bash
$ PGPASSWORD=$(cat ./very-secret.txt) psql \
>   "postgres://initech_master_user@initech-sandbox.cthulhu2hyup.zz-outercentral-7.rds.amazonaws.com:5432/initech"
psql: error: connection to server at "initech-sandbox.cthulhu2hyup.zz-outercentral-7.rds.amazonaws.com" (10.54.42.10), port 5432 failed: FATAL:  permission denied for database "initech"
DETAIL:  User does not have CONNECT privilege.
```

## Detecting issues locally

We never detected this `CONNECT` issue because we were using a superuser in our
Dockerized PostgreSQL instance during local development with the Terraform
[provider][2]. A superuser can **never** get locked out because it can do
anything and everything in the PostgreSQL instance.

To fix this, we introduced an equivalent to the RDS master user locally and
stopped using the superuser from Terraform. After switching to this user
in the Terraform provider, we were able to replicate the `CONNECT` issue.

To create the RDS master user locally, we jumped on an RDS instance and examined
the attributes of the RDS master user:

```sql
initech=> \du initech_master_user
                             List of roles
      Role name      |          Attributes           |    Member of
---------------------+-------------------------------+-----------------
 initech_master_user | Create role, Create DB       +| {rds_superuser}
                     | Password valid until infinity |

initech=> SELECT * FROM pg_catalog.pg_roles WHERE rolname = 'initech_master_user';
       rolname       | rolsuper | rolinherit | rolcreaterole | rolcreatedb | rolcanlogin | rolreplication | rolconnlimit | rolpassword | rolvaliduntil | rolbypassrls | rolconfig |  oid
---------------------+----------+------------+---------------+-------------+-------------+----------------+--------------+-------------+---------------+--------------+-----------+-------
 initech_master_user | f        | t          | t             | t           | t           | f              |           -1 | ********    | infinity      | f            |           | 13370
(1 row)

```

Using this information, we created an SQL file (`rds_master_user.sql`) to
create this role in the Dockerized PostgreSQL instance:

```sql
CREATE ROLE initech_master_user
  WITH ENCRYPTED PASSWORD '...'
  VALID UNTIL 'infinity'
  NOSUPERUSER
  INHERIT
  CREATEROLE
  CREATEDB
  LOGIN
  NOREPLICATION
  CONNECTION LIMIT -1
  NOBYPASSRLS;
```

In order to ensure this role gets created during PostgreSQL startup, we
volume mount it at `/docker-entrypoint-initdb.d/rds_master_user.sql`.

## Fixing the issue

In order to fix the broken RDS instance, we temporarily granted the admin
role to the RDS master user:

```sql
GRANT lumbergh TO initech_master_user;
-- AFTER: REVOKE lumbergh FROM initech_master_user;
```

and made sure the master user could connect as well:

```hcl
locals {
  aws_master_user = "initech_master_user"
}

resource "postgresql_grant" "aws_master_user_connect" {
  database    = postgresql_database.initech.name
  role        = local.aws_master_user
  object_type = "database"
  privileges  = ["CONNECT"]
}
```

## Conclusion

Subtle behavior differences between local development and production can lead to
not-so-subtle issues. There is a long tail of problems that can arise if the
development setup is too different, particularly issues around permissions.

Emulating the PostgreSQL RDS master user allows Terraform to manage roles
locally in the same way they are managed in production. This is just one of many
changes needed to make the local development database faithful to production.
Luckily, using Terraform locally allows us to bridge **many** other gaps by
giving us the same roles and grants that we have in RDS.

<div markdown="1" style="text-align: center;">
  ![Bill Lumbergh; Initech](/images/lumbergh.png)
</div>

[1]: https://www.terraform.io/
[2]: https://registry.terraform.io/providers/cyrilgdn/postgresql
[3]: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.MasterAccounts.html
[4]: https://en.wikipedia.org/wiki/Data_definition_language
[5]: https://en.wikipedia.org/wiki/Data_manipulation_language
[6]: https://engineering.hardfin.com/2022/04/emulate-rds-permissions/
