---
title: Wrapping Behavior of `context.WithValue()`
date: 2021-09-10
author: Danny Hermes (dhermes@bossylobster.com)
tags: Go, Golang, Context
slug: go-context-withvalue
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2021-09-10-go-context-withvalue.md
---

### Motivation

Throughout the Go monorepo we use `context.WithValue()` to "stash" a global
value on a root context. For example

```go
ctx = logger.WithLogger(ctx, log)
// ... later ...
log := logger.GetLogger(ctx)
```

The implementations for stashing a `logger.Log` are in the same general form
as most context wrapping helpers:

```go
type loggerKey struct{}

func WithLogger(ctx context.Context, log Log) context.Context {
	return context.WithValue(ctx, loggerKey{}, log)
}

func GetLogger(ctx context.Context) Log {
	if value := ctx.Value(loggerKey{}); value != nil {
		if typed, ok := value.(Log); ok {
			return typed
		}
	}
	return nil
}
```

Our goal here is to understand how `context.WithValue()` keeps the
data around and how `ctx.Value()` is able to extract it back out.

### Dealing with Unexported Types

In addition, to defining the `context.Context` interface, the Go standard
library also defines some unexported concrete implementations. In particular,
`emptyCtx` is [defined][1] to support `context.Background()` and `valueCtx`
is [defined][2] to support `context.WithValue()`.

In order to see **inside** values of each of these types, we can create
a sufficiently similar type and then use the `reflect` and `unsafe` packages
to "cast" the memory from the standard library types into our own types.
For example:

```go
func CtxPointer(ctx context.Context) *int {
	rc := reflect.ValueOf(ctx)
	p := unsafe.Pointer(rc.Pointer())
	return (*int)(p)
}

func ToEmptyCtx(ctx context.Context) *EmptyCtx {
	p := unsafe.Pointer(CtxPointer(ctx))
	return (*EmptyCtx)(p)
}
```

The fields in the types themselves are straightforward to copy over:

```go
type EmptyCtx int

type ValueCtx struct {
	wrapped  context.Context // Intentionally avoid struct-embedding
	key, val interface{}
}
```

### Unwrapping It All

In order to better understand how context wrapping via `context.WithValue()`
works, we'll stash multiple values for the same key onto a context:

```go
type simpleKey struct{}

func main() {
	ctx1 := context.Background()
	fmt.Printf("ctx1 = %s\n", ToEmptyCtx(ctx1))
	fmt.Printf("  ctx1.Value(simpleKey{}) = %v\n", ctx1.Value(simpleKey{}))
	// Wrap once.
	ctx2 := context.WithValue(ctx1, simpleKey{}, "x")
	fmt.Printf("ctx2 = %s\n", ToValueCtx(ctx2))
	fmt.Printf("  ctx2.Value(simpleKey{}) = %q\n", ctx2.Value(simpleKey{}))
	// Wrap twice.
	ctx3 := context.WithValue(ctx2, simpleKey{}, "y")
	fmt.Printf("ctx3 = %s\n", ToValueCtx(ctx3))
	fmt.Printf("  ctx3.Value(simpleKey{}) = %q\n", ctx3.Value(simpleKey{}))
	// Wrap thrice.
	ctx4 := context.WithValue(ctx3, simpleKey{}, "z")
	fmt.Printf("ctx4 = %s\n", ToValueCtx(ctx4))
	fmt.Printf("  ctx4.Value(simpleKey{}) = %q\n", ctx4.Value(simpleKey{}))
}
```

Running the script we see that the **latest** value stashed for the key
wins in `valueCtx.Value()`. We also see that the second stage (`ctx2`)
wraps the first (`0xc00009e000`), the third stage (`ctx3`) wraps the second
(`0xc0000981b0`) and so on.

```text
$ go run docs/go-context-withvalue/main.go
ctx1 = EmptyCtx(0) [address=0xc00009e000]
  ctx1.Value(simpleKey{}) = <nil>
ctx2 = ValueCtx(wrapped=0xc00009e000, key=main.simpleKey{}, val="x") [address=0xc0000981b0]
  ctx2.Value(simpleKey{}) = "x"
ctx3 = ValueCtx(wrapped=0xc0000981b0, key=main.simpleKey{}, val="y") [address=0xc0000981e0]
  ctx3.Value(simpleKey{}) = "y"
ctx4 = ValueCtx(wrapped=0xc0000981e0, key=main.simpleKey{}, val="z") [address=0xc000098210]
  ctx4.Value(simpleKey{}) = "z"
```

[1]: https://github.com/golang/go/blob/go1.17.1/src/context/context.go#L171
[2]: https://github.com/golang/go/blob/go1.17.1/src/context/context.go#L538
