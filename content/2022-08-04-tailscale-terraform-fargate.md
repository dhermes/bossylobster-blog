---
title: Managing Tailscale subnet routers with Terraform
description: Releasing a Terraform module for deploying a Tailscale subnet router with AWS ECS Fargate and managing the resources via Terraform.
date: 2022-08-04
author: Danny Hermes (dhermes@bossylobster.com)
tags: Tailscale, ECS, Fargate, Serverless, Terraform, Open Source
slug: tailscale-terraform-fargate
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/tailscale-terraform-fargate.png
github_slug: content/2022-08-04-tailscale-terraform-fargate.md
---

<div markdown="1" style="text-align: center;">
  ![Tailscale, Terraform, and Fargate](/images/tailscale-terraform-fargate.png)
</div>

> This is cross-posted from the Hardfin engineering [blog][17].

As a small and growing team, we need to focus our operational efforts as much as
possible. Using [Tailscale][1] as our VPN is very much aligned with this need.
It's simple, with no central control plane to manage or other significant
operational burden for our team.

In addition to providing a secure internal network for peer-to-peer
communications, Tailscale enables us to securely access databases and services
deployed in our AWS accounts via [subnet routers][2].

We run one subnet router per AWS VPC as an ECS [Fargate][3] task and manage
the deployment with Terraform. Today we are releasing the
`hardfinhq/tailscale-subnet-router` Terraform [module][4] to share our tools
for managing subnet routers.

## Why Tailscale?

Nearly every day I see a new Tailscale user tweeting that they can't believe how
quick and easy it is to set up. One of the biggest hallmarks of Tailscale is
one we hope to emulate at Hardfin: it **just works**.

Our primary use case for a VPN is secure access to deployed environments.
However, Tailscale also enables a new kind of lightweight collaboration for
distributed teams. The peer-to-peer nature of a mesh VPN allows our team to
share workspaces and run low fidelity internal services with almost no effort:

- Working on a branch and want to share `localhost:3000` with the team? Just
  bind your webserver to `0.0.0.0`[ref]Or your `100.x.y.z` [Tailscale IP][16] if
  you'd like to be more surgical when binding to network interfaces.[/ref] and
  share a link using your machine's magic DNS name, e.g.
  `fuzzy.hardfinhq.org.github.beta.tailscale.net`.
- Need a place to serve developer docs (`godoc -http=:6060`) without the cost or
  complexity of the cloud? Park a bare metal server in a closet and connect it
  to your Tailnet.
- Want static code coverage reports in `main` for the team to keep an eye on
  quality over time? SSH into that bare metal server and add another static
  site.

Not only do we love the feature set, we also have a mountain of respect for the
Tailscale team. Tailscale is filled with internet OGs that have experience
running large networks, infrastructure at hyperscalers, and developing and
deploying [WireGuard][5]. This experience manifests in the product: Tailscale
continues to work in [thorny][6] networking conditions when most other VPNs
are not able to. Their ability to clearly communicate
[deep technical ideas][7] is also one we hope to emulate right here in our
engineering blog.

## Why Fargate?

Running the services used by our customers is our core operational charter. The
overhead of anything else must be carefully weighed and usually our answer is to
live without tools that have **any** operational overhead.

For example, our founding team has deep experience with HashiCorp Vault, but we
decided not to use it because **someone** would need to hold the pager. Instead
we use [AWS Secrets Manager][8] for secrets and [AWS KMS][9] for transit
encryption. Though the HashiCorp Vault feature set is more robust, the added
benefit isn't worth the cost of running Vault with a small team.

ECS Fargate really fits our philosophy and delivers on the promise of the cloud.
It is serverless in the sense that we care about: we don't have a
cluster[ref]Our founding team has deep experience with Kubernetes as well but
chose not to use it because of the operational burden. An ECS task definition is
**very** similar to a Kubernetes pod spec already, so we get many of the same
benefits afforded by Kubernetes.[/ref] or compute nodes (i.e. servers) to
administer. Fargate provides a great blend of flexibility and focus. Though
[Firecracker][10] is used to enable serverless at AWS in both Fargate and
Lambda, we prefer the flexibility of Docker containers and the control afforded
by long-lived processes over the FaaS model.

## Using the module

As we've mentioned [previously][11], we are big proponents of
Infrastructure-as-Code at Hardfin. With the `hardfinhq/tailscale-subnet-router`
[module][4], we are able to define all of the resources needed for a subnet
router declaratively. We can easily add a subnet router every time we bring up a
new VPC. For example:

```hcl
module "sandbox" {
  source  = "hardfinhq/tailscale-subnet-router/aws"
  version = "1.20220802.1"

  vpc                         = "sandbox"
  subnet_group                = "sandbox-igw-zz-minotaur-7"
  security_group_ids          = [data.aws_security_group.vpn.id]
  target_ecs_cluster          = "sandbox-spot"
  tailscale_auth_key_secret   = "sandbox-tailscale-auth-key"
  tailscale_docker_repository = "tailscale"
  tailscale_docker_tag        = "sha-a0063fef6ccfa4dc689642d60637a124c60b1be3"
}

data "aws_security_group" "vpn" {
  name = "sandbox-vpn"
}
```

This only requires a few prerequisites to be in place:

- A Tailscale [auth key][12] stored in an AWS Secrets Manager secret
- A Docker image tagged and pushed to ECR for running your subnet router; we
  have provided a [Dockerfile][13] you can use
- The core foundation needed for an ECS cluster that can schedule Fargate tasks
  (i.e. the cluster, a VPC, subnets, security groups, etc.)

## Onwards

We'd love to continue the discussion [on GitHub][14]. Feature requests and pull
requests are welcome! For the initial release, the module is very much scoped to
our internal networks at Hardfin but we'd be happy to make the module more
configurable to make it accessible to a broader audience. There are a few
[suggestions][15] already in the repository as a starting point for ways to
help adapt the module to other engineering organizations.

[1]: https://tailscale.com/
[2]: https://tailscale.com/kb/1019/subnets/
[3]: https://aws.amazon.com/fargate/
[4]: https://registry.terraform.io/modules/hardfinhq/tailscale-subnet-router
[5]: https://www.wireguard.com/
[6]: https://tailscale.com/blog/how-nat-traversal-works/
[7]: https://tailscale.com/blog/how-tailscale-works/
[8]: https://aws.amazon.com/secrets-manager/
[9]: https://aws.amazon.com/kms/
[10]: https://firecracker-microvm.github.io/
[11]: /2022/04/emulate-rds-permissions
[12]: https://tailscale.com/kb/1085/auth-keys/
[13]: https://github.com/hardfinhq/terraform-aws-tailscale-subnet-router/blob/v1.20220802.1/_docker/tailscale.Dockerfile
[14]: https://github.com/hardfinhq/terraform-aws-tailscale-subnet-router/issues/new
[15]: https://github.com/hardfinhq/terraform-aws-tailscale-subnet-router/tree/v1.20220802.1#room-for-improvement
[16]: https://tailscale.com/kb/1015/100.x-addresses/
[17]: https://engineering.hardfin.com/2022/08/tailscale-terraform-fargate/
