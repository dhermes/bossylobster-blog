---
title: Type Guards for Union Types in TypeScript
description: Getting Some Help from the TypeScript compiler
date: 2019-06-09
author: Danny Hermes (dhermes@bossylobster.com)
tags: Programming, TypeScript, Types
slug: type-guards-for-union-types
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2019-06-09-type-guards-for-union-types.md
---

In my day job at [Blend][1], I write a lot of TypeScript[ref]This may surprise
many of my colleagues from the Python world[/ref]. One great feature of
TypeScript is the ability to specify an enum with a finite set of values
as a [union type][2]:

```typescript
type Coordinate = 'x' | 'y'
```

which then gives compile time checking for values of this type

```typescript
const coordinate: Coordinate = 'x'
// This will not compile: const coordinate: Coordinate = 'donut'
```

### Contents

- [What's Missing](#whats-missing)
- [What Can Go Wrong](#what-can-go-wrong)
- [How Can We Fix It](#how-can-we-fix-it)
- [But What About ...](#but-what-about)
- [Related Approaches](#related-approaches)

### What's Missing {#whats-missing}

Unfortunately, there is no utility built into the language that will provide
an array of the values in the union type. I.e. for our `Coordinate` type, we
often want:

```typescript
const COORDINATES: Coordinate[] = ['x', 'y']
// Or even better, make it immutable: Object.freeze(['x', 'y'])
```

Such a `COORDINATES` array has many uses. It's common to use such an array
to write a [type guard][3]

```typescript
function isCoordinate(value: string): value is Coordinate {
  return COORDINATES.includes(value)
}
```

or to specify a [`Joi` schema][4] for an external facing API:

```typescript
import * as Joi from '@hapi/joi'

const REPLACE_VALUE: Joi.ObjectSchema = Joi.object({
  id: Joi.string().guid().required(),
  coordinate: Joi.string().valid(COORDINATES).required(),
  value: Joi.number().required(),
})
```

### What Can Go Wrong {#what-can-go-wrong}

It's easy enough to just hardcode `COORDINATES` to exactly agree with your
`Coordinate` union type and feel happy that it's a comprehensive coverage of
the values. Even better, since `COORDINATES` has the type `Coordinate[]`, you
have a guarantee[ref]Provided you don't use any
`as Coordinate[]` [type assertion][5] funny business[/ref] from the `tsc`
compiler that you won't have any invalid values.

However, let's say one day your codebase decides to expand from 2D into 3D:

```typescript
type Coordinate = 'x' | 'y' | 'z'
```

None of the rest of your code will break, but it **should have**! Your
`COORDINATES` covering set is no longer a covering set, but both `x` and `y`
are valid. Calling `isCoordinate('z')` will return `false` (which is a lie)
and your `REPLACE_VALUE` schema will reject calls to your API that want to
replace the `z` value.

### How Can We Fix It {#how-can-we-fix-it}

By hardcoding `COORDINATES` we've accidentally made our codebase brittle. The
`['x', 'y']` [literal][11] encodes an **assumption** about our code that is not
checked anywhere at all. Also, the `tsc` compiler has no hope in helping us
because `COORDINATES` is a **value**, not a **type**, so `tsc` isn't able to
make any extra assertions to act as a guard rail.

Unit tests to the rescue! We can write a single unit test ([with `ava`][6])
that is guaranteed to fail if either the `Coordinate` union type or the
`COORDINATES` value is changed:

```typescript
import test from 'ava'

test('COORDINATES covers the Coordinate union type', t => {
  const asKeys: Record<Coordinate, number> = { x: 0, y: 0 }
  const expectedKeys = Object.keys(asKeys).sort()
  // NOTE: Sort `COORDINATES` without mutating it.
  const actualKeys = COORDINATES.concat().sort()
  t.deepEqual(expectedKeys, actualKeys)
})
```

Using the [`Record<>` type][7] allows the **compiler** to tell us if any
members of the `Coordinate` are absent keys in `asKeys`. Then at **runtime**
we use `Object.keys()` to convert those (already compiler checked) keys into
a **value** `expectedKeys`. Then we can ensure that `expectedKeys` is verified
against `COORDINATES`.

### But What About ... {#but-what-about}

The snippet in the unit test absolutely provides a template for doing this
inline (i.e. without the support of a unit test):

```typescript
type Coordinate = 'x' | 'y'
const asKeys: Record<Coordinate, number> = { x: 0, y: 0 }
const COORDINATES: Coordinate[] = Object.keys(asKeys)
```

however, this snippet of code will fail due to the return type of
`Object.keys()`:

```console
$ tsc snippet.ts
snippet.ts:6:7 - error TS2322: Type 'string[]' is not assignable to type 'Coordinate[]'.
  Type 'string' is not assignable to type 'Coordinate'.

6 const COORDINATES: Coordinate[] = Object.keys(asKeys)
        ~~~~~~~~~~~


Found 1 error.

```

So in order to use it, you'd need to resort back to a type assertion (and IMO
type assertions should be avoided at all costs).

Additionally, though declaring `asKeys` only takes up one line, it's a bit
of an eyesore in **source** code (vs. **test** code). As the number of allowed
values in a given union type goes up, declaring `asKeys` inline will look even
worse.

### Related Approaches {#related-approaches}

I've also had cases where I had a use in my code for a mapping identical to what
was provided by `Record<>`. It's equally fine to define that mapping
directly and derive the `Coordinate` union type from it via the
[`keyof` keyword][8]

```typescript
interface Point {
  x: number
  y: number
}
type Coordinate = keyof Point
```

Then the unit test will change ever so slightly[ref]In cases where some of the
keys are optional, a `Required<Point>` must be used for the type of `asKeys`.
The `Required<>` type was [added][9] in TypeScript 2.8.)[/ref]

```typescript
const asKeys: Point = { x: 0, y: 0 }
```

In codebases where "no magic constants" is a rule[ref]I.e. typing `'x'` or
`'y'` would not be allowed[/ref], a convenience `enum` can
be provided to give named variables for each value in the `Coordinate` type:

```typescript
enum CoordinateNames {
  x = 'x',
  y = 'y',
}
type Coordinate = keyof typeof CoordinateNames
```

Since a [TypeScript `enum`][10] is really just an `object`, we can use it
directly in our unit test without having to form the stand-in `asKeys` value

```typescript
const expectedKeys = Object.keys(CoordinateNames).sort()
```

[1]: https://blend.com/careers/
[2]: https://www.typescriptlang.org/docs/handbook/advanced-types.html#union-types
[3]: https://www.typescriptlang.org/docs/handbook/advanced-types.html#type-guards-and-differentiating-types
[4]: https://github.com/hapijs/joi
[5]: https://www.typescriptlang.org/docs/handbook/basic-types.html#type-assertions
[6]: https://github.com/avajs/ava
[7]: https://stackoverflow.com/a/51937036/1068170
[8]: https://mariusschulz.com/blog/typescript-2-1-keyof-and-lookup-types
[9]: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-2-8.html
[10]: https://www.typescriptlang.org/docs/handbook/enums.html
[11]: https://en.wikipedia.org/wiki/Literal_(computer_programming)
