---
title: GitHub Actions with Monorepos
date: 2022-02-17T00:00:00-07:00
authors:
- dhermes
tags:
- github-actions
- continuous-integration
- monorepo
hero: github-actions-logo.png
draft: true
---

{{< img "github-actions-logo.png" "GitHub Actions" >}}

The goal of this post is to describe a common CI problem encountered in
monorepos &mdash; **conditionally required** checks &mdash; and to introduce a
GitHub Action that helps to solve this problem. Using a monorepo may not be the
right choice for every engineering organization. For those using a monorepo,
the problem of conditionally required checks will need to be solved eventually.

## Why Choose a Monorepo?

There are many benefits to managing code in a monorepo. For example:

- **Code Sharing**: no need for internal package management (e.g. running an
  internal `npm` server, Go modules proxy, PyPI server, Maven repository, etc.)
- **Shared Tooling**: organization-wide refactoring, enforcement of best
  practices, unified build improvements
- **External Dependency Management**: central management of dependencies from
  external parties and vendors, including shared vetting
- **Modernization**: full visibility into impacts of breaking changes, old
  code can be removed once unused

Of course a monorepo [isn't][1] a panacea. For example, it still requires
discipline to organize code with logical boundaries or to track interface
breakages that impact **running code**[^running-code].

## Conditionally Required Status Checks

Using a monorepo requires more effort to overcome problems that just don't
exist with a polyrepo approach. For example, a monorepo requires a larger
investment in local development tooling e.g. to reuse cached build artifacts or
to limit test suites to only run for modified packages. As an engineering
organization grows, a monorepo may start to stretch the limits of scalability
of the VCS of choice (e.g. `git`).

At Blend and many other companies, continuous integration (CI) gives
confidence when merging code and helps maintain code quality across time.
GitHub provides powerful tools to enforce **required** checks and approvals
from code owners and allows [auto-merge][2] once these requirements
are satisfied:

{{< img "all-checks-required.png" "All Checks Required" >}}

In a monorepo, teams will want to add checks that are specific to their own
code and not relevant for the repository at large. For the example codebase
above, changes to Go source code trigger the `unit-test-go-core` and `lint-go`
checks and changes to Protobuf source code trigger the `lint-protobuf` and
`protobuf-check-generated` checks. But Go-only changes **should not** need to
trigger the Protobuf checks. For a pull request with only Go, this would mean
the Protobuf checks would never run. If all checks were required, this would
leave the pull request in an unmergeable state:

{{< img "checks-required-expected.png" "Required Checks Stuck in Expected" >}}

One possible way to solve this would be to just make all checks
optional[^required-checks]. However, this removes GitHub's ability to block a
merge if one of the checks is failing:

{{< img "all-checks-optional.png" "All Checks Optional" >}}

## Composite Check

Unfortunately, the current GitHub offering doesn't provide a way to mark
checks as required some of the time. While that remains true, we have
created the [Require Conditional Status Checks][3] GitHub Action to fill in the
gaps. When using this action, a single job can be marked as a **required**
check. All other checks can remain optional, with the
"conditional requiredness" enforced by the action. For example if only the Go
checks are triggered, the action will ensure they pass:

{{< img "only-require-conditional-less.png" "Only Require Conditional (Less)" >}}

The only required check here is `require-conditional`. As we can see below,
the action has determined that the `unit-test-go-core` and `lint-go` checks are
required and it polls the status of each check until successful completion:

{{< img "example-run-less-public.png" "Example Run (Less)" >}}

If the Protobuf checks are also triggered, the action will ensure the full
set of checks have passed:

{{< img "only-require-conditional-more.png" "Only Required Conditional (More)" >}}
{{< img "example-run-more-public.png" "Example Run (More)" >}}

## How Does It Work?

In order to use this action, a mapping must be provided which indicates
which paths in the source tree cause a given check to be required. For
the examples above, Go code in `cmd/` or `pkg/` triggers the Go checks and
`.proto` files in `proto/` and generated Go in `pkg/protogen/` trigger the
Protobuf checks.

This action uses the GitHub API to retrieve changed files, similar to
[Get All Changed Files][4] or [Changed files][5]. The
files list is compared against a set of glob paths to determine
if there is a match for a given check. Once that list of matching
checks is determined, the status for each check is polled until completion.

Putting this all together in a workflow:

```yaml
---
name: 'Meta Workflow: Require Conditional Status Checks'

on:
  pull_request:
    branches:
    - main

jobs:
  require-conditional:
    runs-on:
    - ubuntu-20.04

    steps:
    - name: Ensure All Conditional Checks Have Passed
      uses: blend/require-conditional-status-checks@2022.02.04
      with:
        interval: 20s
        checks-yaml: |
          - job: unit-test-go-core
            paths:
            - cmd/**
            - pkg/**
          - job: lint-go
          - job: protobuf-check-generated
            paths:
            - proto/**
            - pkg/protogen/**
          - job: lint-protobuf
            paths:
            - proto/**
```

## Conclusion

Teams that have made the choice to adopt a monorepo have chosen the path
with the benefits in mind. Adopting extra tooling to support a monorepo is
part of that bargain. The [Require Conditional Status Checks][3] GitHub Action
we created allows monorepo-aware enforcement of required checks. Using it, we
can keep the typical CI merge flow that teams love without burdening every pull
request with extra checks unrelated to the code changes.

## Further Reading

### On GitHub Actions

- About custom actions [article][6] from GitHub
- How We Write GitHub Actions in Go [blog post][7] from this same blog

### On Monorepos

- Improving large monorepo performance on GitHub [blog post][8] from
  GitHub in 2021
- Why Google Stores Billions of Lines of Code in a Single Repository
  [talk][9] from @Scale 2015
- Why Google Stores Billions of Lines of Code in a Single Repository
  [paper][10] from Communications of the ACM 2016
- Scaling Mercurial at Facebook [blog post][11] from 2014
- Big Code: Developer Infrastructure at Facebook's Scale [talk][12]
  from F8 2015
- Benefits and challenges of using monorepo development practices
  [blog post][13] from CircleCI in 2021
- Advantages of Monorepos [blog post][14] by Dan Luu from 2015
- Taming Your Go Dependencies [blog post][15] by [Bryan Liles][16]
  and Digital Ocean in 2015

[1]: https://medium.com/@mattklein123/monorepos-please-dont-e9a279be011b
[2]: https://github.blog/changelog/2021-02-04-pull-request-auto-merge-is-now-generally-available/
[3]: https://github.com/marketplace/actions/require-conditional-status-checks
[4]: https://github.com/marketplace/actions/get-all-changed-files
[5]: https://github.com/marketplace/actions/changed-files
[6]: https://docs.github.com/en/actions/creating-actions/about-custom-actions
[7]: /how-we-write-github-actions-in-go.html
[8]: https://github.blog/2021-03-16-improving-large-monorepo-performance-on-github/
[9]: https://www.youtube.com/watch?v=W71BTkUbdqE
[10]: https://research.google/pubs/pub45424/
[11]: https://engineering.fb.com/2014/01/07/core-data/scaling-mercurial-at-facebook/
[12]: https://www.youtube.com/watch?v=X0VH78ye4yY
[13]: https://circleci.com/blog/monorepo-dev-practices/
[14]: https://danluu.com/monorepo/
[15]: https://www.digitalocean.com/blog/taming-your-go-dependencies/
[16]: https://twitter.com/bryanl
[17]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule#creating-a-branch-protection-rule
[^running-code]:
    A monorepo prevents a certain class of interface breakage from being
    merged. However if a breaking update to a service's API is deployed before
    consuming services are deployed, problems will likely occur.
[^required-checks]:
    See the "Managing a branch protection rule" [article][17] for more
    details on the experience. In particular, step 7 discusses how to
    add required checks.
