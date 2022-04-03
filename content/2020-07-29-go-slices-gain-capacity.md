---
title: How Do Slices Gain Capacity in Go?
date: 2020-07-29
author: Danny Hermes (dhermes@bossylobster.com)
tags: Go, Golang, Internals
slug: go-slices-gain-capacity
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2020-07-29-go-slices-gain-capacity.md
---

### Looking Inside a Slice

The first thing to realize is that a `slice` in Go is really just a struct
that wraps "header" information about (1) a pointer to the "real" underlying
data, (2) the length and (3) the capacity without directly exposing those
fields. We can use a `struct` like:

```go
type IntSlice struct {
	Start    *int // (1)
	Length   int  // (2)
	Capacity int  // (3)
}
```

to unpack the fields in use. Putting this in a script:

```go
package main

import (
	"fmt"
	"unsafe"
)

type IntSlice struct {
	Start    *int // (1)
	Length   int  // (2)
	Capacity int  // (3)
}

func FromSlice(ps *[]int) *IntSlice {
	p := unsafe.Pointer(ps)
	return (*IntSlice)(p)
}

func Display(ps *[]int) {
	is := FromSlice(ps)
	fmt.Printf("%#v\n", is)
}

func main() {
	s := make([]int, 0, 3)
	Display(&s)
}
```

we can verify that `IntSlice` accurately describes an `[]int` slice:

```
$ go run docs/go-slices-gain-capacity/unsafe/main.go
&main.IntSlice{Start:(*int)(0xc0000b4020), Length:0, Capacity:3}
```

Note that conversion from `[]int` to `IntSlice` isn't straightforward. It
requires use of the `unsafe` Go package to interact with raw pointers:

```go
func FromSlice(ps *[]int) *IntSlice {
	p := unsafe.Pointer(ps)
	return (*IntSlice)(p)
}
```

### Printing Useful Information

In order to understand how the slice changes when it needs to gain capacity,
it's useful for us to see if the address of the `[]int` slice itself changes
as well as to see if the underlying `Start` address changes. We can update
`Display()` to incorporate this information in a useful way:

```go
func Display(ps *[]int) {
	is := FromSlice(ps)
	s := *ps
	fmt.Printf(
		"s=%v | &s=%p, start=%p, len=%d, cap=%d\n",
		s, ps, is.Start, len(s), cap(s),
	)
}
```

which yields:

```
$ go run docs/go-slices-gain-capacity/useful/main.go
s=[] | &s=0xc0000a6040, start=0xc0000b4020, len=0, cap=3
```

### `append()` Until Capacity Runs Out

Now that we can actually "observe" the underlying data in a slice, we can
continue to use `append()` to grow the slice:

```go
func main() {
	s := make([]int, 0, 3)
	Display(&s)
	for i := 1; i < 8; i++ {
		s = append(s, i*i)
		Display(&s)
	}
}
```

We see that when the capacity changes (from 3 to 6 to 12) the pointer to the
underyling data changes as well (from `0xc0000b4020` to `0xc0000aa060` to
`0xc00008c060`):

```
$ go run docs/go-slices-gain-capacity/exceed/main.go
s=[]                  | &s=0xc0000a6040, start=0xc0000b4020, len=0, cap=3
s=[1]                 | &s=0xc0000a6040, start=0xc0000b4020, len=1, cap=3
s=[1 4]               | &s=0xc0000a6040, start=0xc0000b4020, len=2, cap=3
s=[1 4 9]             | &s=0xc0000a6040, start=0xc0000b4020, len=3, cap=3
s=[1 4 9 16]          | &s=0xc0000a6040, start=0xc0000aa060, len=4, cap=6
s=[1 4 9 16 25]       | &s=0xc0000a6040, start=0xc0000aa060, len=5, cap=6
s=[1 4 9 16 25 36]    | &s=0xc0000a6040, start=0xc0000aa060, len=6, cap=6
s=[1 4 9 16 25 36 49] | &s=0xc0000a6040, start=0xc00008c060, len=7, cap=12
```

As a nice bonus we also see that the address of our slice `s` doesn't change
even though we overwrite it nine times.
