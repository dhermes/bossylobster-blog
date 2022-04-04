---
title: Custom GitHub Actions
date: 2021-03-03
author: Danny Hermes (dhermes@bossylobster.com)
tags: GitHub Actions, GitHub, Actions
slug: custom-github-actions
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2021-03-03-custom-github-actions.md
---

The "obvious" way to write a custom GitHub Action is using Node.js, however
it's not the only way. As it turns out, a GitHub Action really just
communicates with the "orchestrator" via environment variables (as inputs)
and STDOUT (to produce custom outputs).

### Options

When defining an action, there are (as of this writing) three ways to
determine how it gets invoked

```yaml
runs:
  using: node12
  main: index.js
# OR
runs:
  using: docker
  main: Dockerfile
# OR
runs:
  using: composite
  steps:
  - run: ${{ github.action_path }}/main.sh
    shell: bash
```

I was hoping to lean on some mature Go tooling to write an action in Go, so
that ruled out `using: node12`. Additionally, by having a custom `Dockerfile`,
we would force all users of an action to wait through `docker build` on
every invocation of the action. This left `using: composite` as the early
leader.

When running with `using: composite`, I found that my `main.sh` executed just
fine, but there were two problems that made it **not** an
option[ref]Both of these issues may just be a symptom of the version of GitHub
Enterprise we are running, so we can likely revisit[/ref]:

- None of the `INPUT_*` environment variables were passed in to my script
- My `STDOUT` was not being interpreted and used
- The `ACTIONS_RUNTIME_TOKEN` and `ACTIONS_RUNTIME_URL` environment variables
  were absent

### A Path Forward

In order to invoke my shell script **as if** it were `using: node12`, I
introduced the following shim

```javascript
const childProcess = require("child_process");
const process = require("process");

function main() {
  const mainScript = `${__dirname}/main.sh`;
  const spawnSyncReturns = childProcess.spawnSync(mainScript, {
    stdio: "inherit",
  });
  const status = spawnSyncReturns.status;
  if (typeof status === "number") {
    process.exit(status);
  }
  process.exit(1);
}

if (require.main === module) {
  main();
}
```

and just specified

```yaml
runs:
  using: node12
  main: index.js
```

Here `main.sh` can be replaced with **any** binary, so long as it can run on the
current system[ref]This requires knowing the architecture and possibly which
packages are already installed on the machine. I.e. easier said than
done.[/ref]. For example, a Go static binary targeting Linux would likely work.

### GitHub Actions Inputs and Outputs

One of the official ways to implement a GitHub action is the `@actions/core`
package on the `npm` [public registry][3]. However, each method provided
there really wraps primitives that interact with environment variables or
`STDOUT` and it is these primitives that would enable writing an action in
Go, Python or any other language of our choosing.

For each function provided by `@actions/core`[ref]This is as of [version][4]
`1.2.6`.[/ref], see below the equivalent low-level / non-JavaScript equivalent.

#### `core.exportVariable(name: string, val: any): void`

This appends to the file at the location specified by the `${GITHUB_ENV}`
environment variable. For example if we want to set the environment variable
`NEWLY=ADDED` the following three lines would be appended:

```text
NEWLY<<_GitHubActionsFileCommandDelimeter_
ADDED
_GitHubActionsFileCommandDelimeter_
```

> **Note**: In cases where a name has a "protected" character like `:` in it,
> the character will be replaced by `%3A` or the URL / percent encoded
> equivalent. (This means also that `%` must be encoded as `%25`.)

#### `core.setSecret(secret: string): void`

This writes a line to STDOUT of the form:

```text
::add-mask::${secret}
```

#### `core.addPath(inputPath: string): void`

This appends to the file at the location specified by the `${GITHUB_PATH}`
environment variable. This just appends a line with the path to be added.

#### `core.getInput(name: string, options?: InputOptions): string`

This reads from the `${INPUT_[allcaps(name)]}` environment variable and then
**trims** any whitespace via `String.prototype.trim`. For example if `name` is
`'k'` then we look in `${INPUT_K}`. The literal transformation to `name` is

```javascript
`INPUT_${name.replace(/ /g, "_").toUpperCase()}`;
```

#### `core.setOutput(name: string, value: any): void`

Print to `STDOUT`, e.g. `::set-output name=${name}::${value}"`

#### `core.setCommandEcho(enabled: boolean): void`

This prints either `::echo::on` or `::echo::off` to `STDOUT`

#### `core.setFailed(message: string | Error): void`

The message is printed to `STDOUT`, e.g. if the error message is
"Cannot find widget" then we would print

```text
::error::Cannot find widget
```

to STDOUT and the process exits with 1

#### `core.isDebug(): boolean`

Checks if the `${RUNNER_DEBUG}` environment variable is set to `1`

#### `core.debug(message: string): void`

Prints `::debug::${message}` to `STDOUT`

#### `core.error(message: string | Error): void`

Prints `::error::${message}` to `STDOUT`

#### `core.warning(message: string | Error): void`

Prints `::warning::${message}` to `STDOUT`

#### `core.info(message: string): void`

Prints `${message}` to `STDOUT`

#### `core.startGroup(name: string): void`

Prints `::group::${name}` to `STDOUT`

#### `core.endGroup(): void`

Prints `::endgroup::` to `STDOUT`

#### `core.group<T>(name: string, fn: () => Promise<T>): Promise<T>`

Starts and ends a group and then allows `fn` to modify `STDOUT` in between.
For example if `fn` were to print out `::warning::Slow build` then that
given invocation of `core.group('FYI', fn)` would produce

```text
::group::FYI
::warning::Slow build
::endgroup::
```

#### `core.saveState(name: string, value: any): void`

Prints a line to STDOUT containing the name and a JSON-serialized (without
newlines) version of `value`. For example, invoking via

```javascript
core.saveState("config-map", { a: "b\nc", d: 2.718281828459045 });
```

should produce

```text
::save-state name=config-map::{"a":"b\nc","d":2.718281828459045}
```

#### `core.getState(name: string): string`

Reads from the `STATE_${name}` environment variable and returns the empty
string in the absence. Note that no JSON deserialization is attempted.

Also note that unlike for the `INPUT_` environment variable in
`core.getInput()`, there is no sanitization applied to `name`.

### Alternatives

Another possible option (that has not yet been explored) would be to use

```yaml
runs:
  using: docker
  image: docker://alpine:3.13.2
  entrypoint: main.sh
```

Though it would require some testing to see

- which environment variables are present from within the container
- which files / directories (if any) from the action are mounted in the
  container
- how the status code from the container propagates as part of the action
- if STDOUT / STDERR in the container are treated the same way as
  `using: node12` would be

[1]: https://git.blendlabs.com/actions/bash-proof-of-concept
[2]: https://docs.github.com/en/actions/creating-actions/creating-a-composite-run-steps-action
[3]: https://www.npmjs.com/package/@actions/core
[4]: https://www.npmjs.com/package/@actions/core/v/1.2.6
