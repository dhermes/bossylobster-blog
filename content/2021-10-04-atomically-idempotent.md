---
title: Atomically Idempotent
description: Safe Initialization In Concurrent Go
date: 2021-10-04
author: Danny Hermes (dhermes@bossylobster.com)
tags: Go, Atomic, Idempotent
slug: atomically-idempotent
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2021-10-04-atomically-idempotent.md
---

Recently, I was analyzing some initialization code in Go with a [teammate][1].
The value being initialized was meant to be used in concurrent Go, so
initialization had some requirement of atomicity. The code essentially boiled
down to:

```go
func (t *T) Start() {
	if atomic.LoadInt32(&t.State) == Started {
		return // Early Exit
	}

	atomic.StoreInt32(&t.State, Started)
	t.Starting <- Sentinel
}
```

However, we noted that this code is not truly atomic. The read and write of
the `State` value are individually atomic, but they are not atomic
**together**. One way to achieve atomicity here would be to just hold a mutex.
However, our discussion led to another way to avoid the mutex and to continue
to use the `int32` state value.

### Atomicity First {#atomicity-first}

In order to ensure that our goroutine is the **only** one that can trigger
the sentinel event to the `Starting` channel, we need an atomic
compare-and-swap (CAS). This checks that our goroutine was the **first** to
attempt to set the state to `Started` and **only then** send the sentinel
value to the channel:

```go
func (t *T) Start() {
	previous := atomic.LoadInt32(&t.State)
	if previous == Started {
		return
	}

	swapped := atomic.CompareAndSwapInt32(&t.State, previous, Started)
	if !swapped {
		return
	}
	t.Starting <- Sentinel
}
```

### YMMV: Idempotent First {#idempotency-first}

Depending on the design goals of the code, the idempotency may be
a more crucial feature than the atomicity. For example, the code using a
`T` can be constructed in a way that sending **multiple** sentinel values to
the `Starting` channel is safely idempotent. In this case, a race between two
goroutines with the first code would not be problematic because they could
both send a sentinel.

[1]: https://github.com/mat285
