---
title: How to Write GitHub Actions in Go
date: 2022-02-07
author: Danny Hermes (dhermes@bossylobster.com)
tags: Go, GitHub Actions, Continuous Integration, Golang
slug: how-to-write-github-actions-in-go
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/go-with-github-actions.png
github_slug: content/2022-02-07-how-to-write-github-actions-in-go.md
---

![Go with GitHub Actions](/images/go-with-github-actions.png)

I recently[ref]It was recent when I wrote this on February 7, 2022.[/ref] had
the privilege of co-authoring a blog post on the Blend [engineering blog][100]
with my esteemed colleague [Thomas Taylor][101]. I copied this content over
mostly as-is from the [original post][102] but wanted to preserve it here as
well.

### Contents

- [Introduction](#introduction)
- [Authoring an Action: Today's Landscape](#authoring-an-action)
- [How We Release Actions in Go](#how-we-release)
- [How We Write Actions in Go](#how-we-write)
- [Why Not Docker?](#why-not-docker)
- [Conclusion](#conclusion)

### Introduction {#introduction}

Since the [release][1] of GitHub Actions in 2019, GitHub has been heavily
investing in improvements to the CI / CD experience. As part of this
investment, repeatable tasks can be provided as [custom actions][2] and
shared externally with the community or internally within a GitHub Enterprise
instance.

At Blend, we've benefited from adopting GitHub Actions. We have built
tooling that enables writing an action in Go and automates the release
process for actions within our GitHub Enterprise instance. Below, we'll share
the set of unique challenges for running and releasing actions written in Go
and outline our strategies for solving these problems.

### Authoring an Action: Today's Landscape {#authoring-an-action}

GitHub has published lots of tutorials and many fundamental
actions[ref]For example, using [actions/checkout][18] to checkout code and
[actions/cache][19] to cache dependencies to speed up CI runs.[/ref] as
examples. In order to let the community use the same tools, they have released
the `@actions/core` [package][3] on `npm`.

An action is a GitHub repository with a root
`action.yml` file and supporting files. For authors of an action,
the most common choice is to write it [in JavaScript][4] and run the code
natively on the actions runner during the workflow. If that isn't an
option[ref]E.g. for teams that prefer something other than JavaScript.[/ref], a
[Docker container action][5] allows running a Docker image; the image can
either be built directly from a Dockerfile or pulled from a public Docker
registry.

The third option, a [composite][6] action, allows
creating an action as a series of steps (very similar to how jobs work in
a GitHub Actions workflow). This makes it possible to write lightweight
actions&mdash;e.g. with shell scripts. A composite action can even
[reference][7] other actions in those steps.

### How We Release Actions in Go {#how-we-release}

To distribute our actions written in Go, we build static binaries from
the source code and check them into the GitHub repository for the
action.

#### Example

For an action that needs to run on both 64-bit x86 and ARM
machines running Linux or Windows, it would be enough to use six files:

```text
$ tree
.
├── action.yml
├── invoke-binary.js
├── main-linux-amd64-e9d351bd367300ec85b9ba777812c42be2570a64
├── main-linux-arm64-e9d351bd367300ec85b9ba777812c42be2570a64
├── main-windows-amd64-e9d351bd367300ec85b9ba777812c42be2570a64
└── main-windows-arm64-e9d351bd367300ec85b9ba777812c42be2570a64

0 directories, 6 files
```

In order to invoke the **correct** static binary, we use a tiny JavaScript
[shim][8] to determine the current operating system (`GOOS`) and
platform / architecture (`GOARCH`). The shim dispatches the correct static
binary as follows:

```javascript
function chooseBinary() {
    // ...
    if (platform === 'linux' && arch === 'x64') {
        return `main-linux-amd64-${VERSION}`
    }
    // ...
}

const binary = chooseBinary()
const mainScript = `${__dirname}/${binary}`
const spawnSyncReturns = childProcess.spawnSync(mainScript, { stdio: 'inherit' })
```

and in the `action.yml` we just "pretend to be JavaScript" to call out to
our shim:

```yaml
runs:
  using: node16
  main: invoke-binary.js
```

#### Releasing

At Blend, we maintain all Go actions in our internal Go monorepo. We publish
them into the `actions` organization within our GitHub Enterprise
instance. When a Go action is updated, a post-merge step builds static binaries
for the subset of architectures we need to support and pushes a commit directly
to the respective `actions/${ACTION}` repository. For example, changes in the
Go monorepo to code in `project/github-actions/{cmd,pkg}/build-docker-image/`
will result in a commit to the `actions/build-docker-image` repository.

#### Benefits

Using this approach, an action written in Go runs **immediately**
in the same way an action written in JavaScript does. We eliminate the
need for **any** Go dependencies on the actions runner: GitHub only grabs our
`invoke-binary.js` and static binaries. To make the retrieval fast, we go out
of our way to [shrink][9] the static binaries and make a special "release"
branch that contains a minimal set of files to run the
action[ref]This means we don't need to include any Go source code (or `go.mod`,
etc.) in our "release" branch. By the same token, we wouldn't want to check in
compiled static binaries to our "development" branch.[/ref].

Our approach of using prebuilt binaries is the same idea in spirit as the
recommended approach for JavaScript actions. For JavaScript actions, it
is recommended to use the `ncc` [compiler][10] to create a single `index.js`
file. With this **single file** entrypoint, the action just executes
that file without any other setup necessary. Since Go is a compiled language,
there is no direct equivalent of the "I have some source code and an
interpreter" Node.js approach, hence the need for including prebuilt binaries.
Interestingly enough, the `ncc` project lists the Go compiler as one of its
motivations, so there must be something there!

#### Just Go?

This approach can absolutely be used by programming language ecosystems other
than Go. For example, with the Nuitka [compiler][11] for Python, standalone
executables can be produced in the same way. For compiled languages like C++ or
Rust, creating prebuilt binaries can be straightforward.

One unique advantage Go has in this arena is the default mode of creating
[statically linked][24] binaries. This makes it much easier to **just run** on
a new machine without needing[ref]It's worth [mentioning][20]: cgo is not Go.
Generating a static binary when using cgo is possible but much more
challenging. Cross-compiling a static binary is even more challenging.[/ref]
to install or locate dependencies. Additionally, the Go compiler's ability to
[cross-compile][23] binaries from a single development machine is incredibly
useful for the distribution strategy we use here:

```text
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 \
  go build \
  -ldflags="-s -w" \
  -o main-linux-arm64-e9d351bd367300ec85b9ba777812c42be2570a64 \
  .
```

### How We Write Actions in Go {#how-we-write}

#### Small Entrypoint Scripts

As a rule, we try to make `cmd/${ACTION}/main.go` scripts as short as possible
so we can maximize the amount of code that can be tested[ref]Though it is
possible to test code in `package main`, it is not common. This is particularly
challenging for code paths that end with `os.Exit()`.[/ref]:

```go
// FILE: cmd/hypothetical/main.go

package main

import (
	"context"

	githubactions "github.com/sethvargo/go-githubactions"

	"github.com/blend/hypothetical-action/pkg/hypothetical"
)

func run() error {
	ctx := context.Background()
	action := githubactions.New()

	cfg, err := NewFromInputs(action)
	if err != nil {
		return err
	}

	return hypothetical.Run(ctx, cfg)
}

func main() {
	err := run()
	if err != nil {
		action.Fatalf("%v", err)
	}
}
```

#### Separate Configuration Parsing

By loading **all** inputs and configuration at the outset, an action
can be much easier to reason about: once parsed, a single configuration
struct can be passed to the code implementing the business logic. For example:

```go
// FILE: pkg/hypothetical/config.go

type Config struct {
	Role          string
	LeaseDuration time.Duration
}

func NewFromInputs(action *githubactions.Action) (*Config, error) {
	lease := action.GetInput("lease-duration")
	d, err := time.ParseDuration(lease)
	if err != nil {
		return nil, err
	}

	c := Config{
		Role:          action.GetInput("role"),
		LeaseDuration: d,
	}
	return &c, nil
}
```

#### No Globals

The [sethvargo/go-githubactions][12] project provides an idiomatic
Go package that is roughly equivalent to the `@actions/core` JavaScript
[package][3]. We utilize it wherever we can, but try to follow some larger
principles to write testable code.

When writing code that uses the `githubactions` package, a pointer
`action *githubactions.Action` should be used rather than the global wrappers
around the package `defaultAction` [struct][13]. For example:

```go
role := action.GetInput("role")
// // Don't do this:
// role := githubactions.GetInput("role")
```

In order to test code involving GitHub Actions, it's critical to be able to
both control environment variables (these are inputs) and to monitor writes to
STDOUT. In order to do this in tests, both the STDOUT writer and the
`Getenv()` provider can be replaced:

```go
func TestNewFromInputs(t *testing.T) {
	// ...
	actionLog := bytes.NewBuffer(nil)
	envMap := map[string]string{
		"INPUT_ROLE":           "user",
		"INPUT_LEASE-DURATION": "1h",
	}
	getenv := func(key string) string {
		return envMap[key]
	}
	action := githubactions.New(
		githubactions.WithWriter(actionLog),
		githubactions.WithGetenv(getenv),
	)
	// ...
	it.Equal("...", actionLog.String())
}
```

#### Invoking Actions Locally

To sanity check an implementation, it can be quite useful to run an
action **locally** instead of doing a pre-release and waiting on a fully
triggered GitHub Actions workflow. To run an action locally, it's enough to run
the Go script with the correct environment variables.

There are two types of environment variables needed. The first type are
`GITHUB_*` environment variables that come with the
workflow. The other type are inputs that are provided
in `inputs:` to the action (i.e. the inputs from `action.yml`), which get
transformed into `INPUT_*` environment variables by GitHub.

For example[ref]For action inputs in `kebab-case`, the corresponding
environment variable will have a hyphen, e.g. `INPUT_LEASE-DURATION`. Using
environment variable names with a hyphen requires a little bit of extra care
in most shells, hence the usage of `env INPUT_LEASE-DURATION=...`. [/ref]:

```text
env \
  'GITHUB_API_URL=https://api.github.com' \
  'GITHUB_REPOSITORY=blend/repo-that-uses-an-action' \
  'INPUT_ROLE=user' \
  'INPUT_LEASE-DURATION=1h' \
  go run ./cmd/hypothetical/main.go
```

### Why Not Docker? {#why-not-docker}

Using prebuilt static binaries is not the only choice for writing an
action. We explicitly considered using a Docker container action or a
composite action but elected not to use either.

#### Using a Docker Action

The first obvious choice here would be to write a Dockerfile for the Go
code and use a Docker container action. For example, the GitHub Actions
[tutorial][14] at GopherCon 2021 recommended this approach as do the
[publishing][15] instructions for the `githubactions` package. However, this
experience is not as smooth as the JavaScript one.

With a Docker container action, the image reference can either be a Dockerfile
or an image in a container registry. Referencing a Dockerfile directly
incurs a large cost: every[ref]It's certainly possible to [use][22]
[actions/cache][19] to reuse a Docker build context across workflow runs, but
it is not easy to get right. This puts an unnecessary burden on users of an
action. [/ref] invocation of the action requires the image to be built. Pulling
an image from a public container registry emulates the snappy "run it now"
behavior of JavaScript actions. For images stored in a **private** container
registry, this creates a new challenge. To use an action referencing a private
image, users would need to first authenticate to a registry to pull an image
that they didn't even know they were using:

```yaml
steps:
- name: Login to ECR
  uses: docker/login-action@v1
  with:
    registry: ${{ env.AWS_ACCOUNT_NUMBER }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com
    username: ${{ secrets.AWS_ACCESS_KEY_ID }}
    password: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

- name: Invoke Hypothetical
  uses: blend/hypothetical-action@main
  with:
    role: user
    lease-duration: 1h
```

For internal actions used within an engineering organization
(e.g. within a GitHub Enterprise instance) it's very likely that most images
will be in a private container registry.

#### Using a Composite Action

It is possible to avoid the overhead of Docker build and authentication by
using a composite action. Starting from Go source code[ref]"Starting from Go
source code" as opposed to the other approach, i.e. just distributing prebuilt
binaries. [/ref], the only option is to compile and run that code. This means a
composite action needs to ensure Go is installed on the actions runner. For
example:

```yaml
runs:
  using: composite
  steps:
  - uses: actions/setup-go@v2
    with:
      go-version: '1.17.6'

  - run: go run ./main.go
```

However, this has the same problem as the approach of building a Dockerfile
before running it: the default usage (no caching) involves a significant
cost waiting for build before the action actually runs. What's more,
running [actions/setup-go][16] on the actions runner may overwrite an existing
version of Go installed by the workflow job actually invoking this action,
causing invisible breakage in workflows using this action.

### Conclusion {#conclusion}

Using a tiny JavaScript shim, actions written in Go can be on equal
footing with native JavaScript actions. As we discussed above, there are many
benefits that come from this first-class native support&mdash;chiefly speed of
invocation and simplicity of setup. Best of all, this allows us to bring all
the benefits of Go when writing an action. For internal
actions within an engineering organization, this allows us to reuse existing
Go libraries within our actions. With GitHub Actions and Go, we **can**
have our cake and eat it too.

![Go; now with Cake!](/images/gopher-cake-art.png)

[1]: https://github.blog/2019-08-08-github-actions-now-supports-ci-cd/
[2]: https://docs.github.com/en/actions/creating-actions/about-custom-actions
[3]: https://www.npmjs.com/package/@actions/core
[4]: https://docs.github.com/en/actions/creating-actions/creating-a-javascript-action
[5]: https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
[6]: https://docs.github.com/en/actions/creating-actions/creating-a-composite-action
[7]: https://github.blog/changelog/2021-08-25-github-actions-reduce-duplication-with-action-composition/
[8]: /code/invoke-binary.js
[9]: https://words.filippo.io/shrink-your-go-binaries-with-this-one-weird-trick/
[10]: https://github.com/vercel/ncc
[11]: https://nuitka.net/
[12]: https://github.com/sethvargo/go-githubactions
[13]: https://github.com/sethvargo/go-githubactions/blob/v0.5.1/actions_root.go#L20
[14]: https://github.com/the-gophers/go-action
[15]: https://github.com/sethvargo/go-githubactions/tree/v0.5.2#publishing
[16]: https://github.com/actions/setup-go
[18]: https://github.com/actions/checkout
[19]: https://github.com/actions/cache
[20]: https://dave.cheney.net/2016/01/18/cgo-is-not-go
[22]: https://docs.github.com/en/actions/advanced-guides/caching-dependencies-to-speed-up-workflows
[23]: https://www.digitalocean.com/community/tutorials/building-go-applications-for-different-operating-systems-and-architectures
[24]: https://www.arp242.net/static-go.html
[100]: https://full-stack.blend.com/
[101]: https://github.com/thomasnotfound
[102]: https://full-stack.blend.com/how-we-write-github-actions-in-go.html
