Title: Conway's Topograph Part 1
date: 2011-08-23
author: Danny Hermes (dhermes@bossylobster.com)
tags: Algebra, Binary Quadratic Form, Conway, Conway's Topograph, Math, Number Theory
slug: conways-topograph-part-1

This is the first in a series of three blog posts. In the following
we'll investigate a few properties of an object called Conway's
topograph. [John
Conway](http://en.wikipedia.org/wiki/John_Horton_Conway) conjured up a
way to understand a binary quadratic form &ndash; a very important algebraic
object &ndash; in a geometric context. This is by no means original work, just
my interpretation of some key points from his[The Sensual (Quadratic)
Form](http://www.amazon.com/Sensual-Quadratic-Carus-Mathematical-Monographs/dp/0883850303)that
I'll need for some other posts.


* * * * *



<div class="p1">

</div>

<div class="p1">

**Definition**: A binary quadratic form \\(f\\) is an equation of the
form:

</div>

<div class="p1">

\\[f(x, y) = A x\^2 + H x y + B y\^2.\\]

</div>

<div class="p1">

That is, a function of two variables which is homogeneous of degree two.
The coefficients \\(A\\), \\(H\\), and \\(B\\) and variables \\(x\\) and
\\(y\\) are often real numbers, rational numbers or integers.<span
class="Apple-style-span">\\(\\Box\\)</span>

</div>

<div class="p1">

<span class="Apple-style-span">
</span>

</div>

<div class="p1">

<span class="Apple-style-span"></span>

</div>

<div class="p1">

<span class="Apple-style-span">When we require the coefficients \\(A\\),
\\(H\\), and \\(B\\) as well as the variables \\(x, y\\) to be integers,
we get an integer--valued form. In his *Disquisitiones Arithmeticae*,
Gauss asked (and largely answered) the fundamental question: what
integer values can each form take? For example, you may have seen the
form</span>

</div>

<div class="p1">

<span class="Apple-style-span">\\[f(x, y) = x\^2 + y\^2,\\]</span>

</div>

<div class="p1">

<span class="Apple-style-span">where it was determined that the only
primes (Gaussian primes) occuring were \\(2\\) and those odd primes
congruent to 1 modulo 4.</span>

</div>

<div class="p1">

<span class="Apple-style-span">
</span>

</div>

<div class="p1">

<span class="Apple-style-span">As each form \\(f\\) is homogenous degree
two, \\(f(\\lambda x, \\lambda y) = \\lambda\^2 f(x, y)\\). As a result,
if we can understand the values of \\(f\\) for pairs \\((x, y)\\) which
don't share any factors, we can understand the entire set of values that
\\(f\\) takes. Also, letting \\(\\lambda = -1\\), there is no change in
the value of \\(f\\) since \\(\\lambda\^2 = 1\\), hence it suffices to
think of \\(v = (x, y)\\) as \\(\\pm v\\), i.e. \\(\\left\\{(x, y), (-x,
-y)\\right\\}\\).</span>

</div>

<div class="p1">

<span class="Apple-style-span">
</span>

</div>

<div class="p1">

<span class="Apple-style-span">For integers \\(x\\) and \\(y\\), any
point \\((x, y)\\) can be expressed as an integral linear combination of
the vectors \\(e\_1 = (1, 0)\\) and \\(e\_2 = (0, 1)\\). So if we like,
we can express all relevant inputs for \\(f\\) in terms of two vectors.
However, instead considering \\(e\_2 = (1, 1)\\), we have</span>

</div>

<div class="p1">

<span class="Apple-style-span">\\[(x - y) \\cdot e\_1 + y \\cdot e\_2 =
(x, y)\\]</span>

</div>

<div class="p1">

<span class="Apple-style-span">and realize a different pair \\(e\_1,
e\_2\\) which again yield all possible integer valued vectors as
integral linear combinations.</span>

</div>

<div class="p1">

<span class="Apple-style-span">
</span>

</div>

<div class="p1">

</div>

<div class="p1">

<span class="Apple-style-span">**Definition**:A *strict base*is an
ordered pair \\((e\_1, e\_2)\\) whose integral linear combinations are
exactly all vectors with integer coordinates. A *lax base*is a set
\\(\\left\\{\\pm e\_1, \\pm e\_2\\right\\}\\) obtained from a strict
base.\\(\\Box\\)</span>

</div>

<div class="p1">

<span class="Apple-style-span">
</span>

</div>

<div class="p1">

<span class="Apple-style-span">**Definition**:A *strict superbase*is
an ordered triple \\((e\_1, e\_2, e\_3)\\), for which \\(e\_1 + e\_2 +
e\_3 = (0, 0)\\) and \\((e\_1, e\_2)\\) is a strict base (i.e., with
strict vectors), and a *lax superbase*is a set\\(\\langle\\pm e\_1,
\\pm e\_2, \\pm e\_3\\rangle\\) where \\((e\_1, e\_2, e\_3)\\) is a
strict superbase.\\(\\Box\\)</span>

</div>

<div class="p1">

<span class="Apple-style-span">
</span>

</div>

<div class="p1">

<span class="Apple-style-span">For our (and Conway's) purposes, it is
useful to consider the lax notions and leave the strict notions as an
afterthought since a binary quadratic form is unchanged given a sign
change. From here forward, for a vector \\(v\\), we use the notation
\\(v\\) interchangeably with \\(\\pm v\\) and when referring to a
base/superbase, we are referring to the lax equivalent of these
notions.</span>

Follow along to [Part
2](http://blog.bossylobster.com/2011/08/conways-topograph-part-2.html).

**Update**: *This material is intentionally aimed at an intermediate
(think college freshman/high school senior) audience. One can go deeper
with it, and I'd love to get more technical off the post.*

</div>

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
