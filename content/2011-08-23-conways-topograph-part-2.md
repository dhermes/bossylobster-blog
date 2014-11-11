Title: Conway's Topograph Part 2
date: 2011-08-23 14:00
author: Danny Hermes (dhermes@bossylobster.com)
tags: Algebra, Binary Quadratic Form, Conway, Conway's Topograph, Math, Number Theory
slug: conways-topograph-part-2

This is the second (continued from[Part
1](http://blog.bossylobster.com/2011/08/conways-topograph-part-1.html))in
a series of three blog posts. In the following we'll investigate a few
properties of an object called Conway's topograph.[John
Conway](http://en.wikipedia.org/wiki/John_Horton_Conway)conjured up a
way to understand a binary quadratic form &ndash; a very important algebraic
object &ndash; in a geometric context. This is by no means original work, just
my interpretation of some key points from his[The Sensual (Quadratic)
Form](http://www.amazon.com/Sensual-Quadratic-Carus-Mathematical-Monographs/dp/0883850303)that
I'll need for some other posts.


* * * * *


In the following, as mentioned in Part 1, "when referring to a
base/superbase, we are referring to the lax equivalent of these
notions."

To begin to form the topograph, note each superbase \\(\\left\\{e\_1,
e\_2, e\_3\\right\\}\\) contains only three bases
\\[\\left\\{e\_1, e\_2\\right\\}, \\left\\{e\_2, e\_3\\right\\},
\\left\\{e\_3, e\_1\\right\\}\\]
as subsets. Going the other direction, a base \\(\\left\\{e\_1,
e\_2\\right\\}\\) can only possibly be contained as a subset of two
superbases:
\\[\\langle e\_1, e\_2, (e\_1 + e\_2)\\rangle, \\langle e\_1, e\_2,
(e\_1 - e\_2)\\rangle.\\]
With these two facts in hand, we can begin to form the geometric
structure of the topograph. The interactions between bases and
superbases (as well as the individual vectors themselves) give us the
form. In the graph, we join each superbase (\\(\\bigcirc\\)) to the
three bases (\\(\\square\\)) in it.

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/conway_edges_nodes.png)](http://www.bossylobster.com/images/blog/conway_edges_nodes.png)

</div>

Each edge connecting two superbases (\\(\\bigcirc\\)) represents a base
and we mark each of these edges with a (\\(\\square\\)) in the middle.
Since each base can only be in two superbases, we have well--defined
endpoints for each base (edge). Similarly, since each superbase contains
three bases as subsets, each superbase (endpoint) has three bases
(edges) coming out of it.

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/conway_face.png)](http://www.bossylobster.com/images/blog/conway_face.png)

</div>

As we traverse each edge (base) surrounding a given vector (\\(e\_1\\)
above), we move from superbase (vertex) to superbase (vertex), and form
a face. Starting from a base \\(e\_1, e\_2\\), traveling along each of
the new faces encountered we begin to form the full (labeled) topograph
below:

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/conway_growing_graph.png)](http://www.bossylobster.com/images/blog/conway_growing_graph.png)

</div>

Notice the *values* of \\(f\\) on the combinations of \\(e\_1\\) and
\\(e\_2\\) is immaterial to the above discussion, hence the shape of the
topograph doesn't depend on \\(f\\).

If we know the values of \\(f\\) at some superbase, it is actually
possibly to find the values of \\(f\\) at vectors (faces) we encounter
on the topograph without actually knowing \\(f\\).

**Claim**:For vectors \\(v\_1, v\_2\\),
\\[f(v\_1 + v\_2) + f(v\_1 - v\_2) = 2\\left(f(v\_1) +
f(v\_2)\\right)\\]
**Proof**: Exercise. (If you really can't get it, let me know in the
comments.) \\(\\Box\\)

This implies that if
\\[a = f(v\_1), \\quad b = f(v\_2), \\quad c = f(v\_1 + v\_2), \\quad d
= f(v\_1 - v\_2)\\]
then \\(d\\), \\(a + b\\), \\(c\\) form an arithmetic progression with
common difference \\(h\\). This so--called *Arithmetic Progression
Rule*allows us to mark each edge with a direction based on the value of
\\(h\\). Hence if \\(d \< a + b \< c\\), we have \\(h \> 0\\) and the
following directed edge:

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/conway_directed_edge.png)](http://www.bossylobster.com/images/blog/conway_directed_edge.png)

</div>

<div class="separator" style="clear: both; text-align: left;">

</div>

<div class="separator" style="clear: both; text-align: left;">

Obviously starting from a base \\(e\_1, e\_2\\), one wonders if it is
possible to move to any pair \\((x, y)\\) with \\(x\\) and \\(y\\)
coprime along the topograph. It turns out that we can; the topograph
forms a structurecalled a tree, and all nodes are connected.

</div>

<div class="separator" style="clear: both; text-align: left;">



</div>

<div class="separator" style="clear: both; text-align: left;">

**Lemma**: (Climbing Lemma) Given a superbase \\(Q\\) with the
surrounding faces taking values \\(a\\), \\(b\\), and \\(c\\) as below,
if the \\(a\\), \\(b\\) and the common difference \\(h\\) are all
positive, then \\(c\\) is positive and the other two edges at
\\(Q\\)point away from \\(Q\\).

</div>

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/conway_directed_edge_superbase.png)](http://www.bossylobster.com/images/blog/conway_directed_edge_superbase.png)

</div>

**Proof**:First \\(c\\) is positive because \\(h = c - (a + b)\\),
hence \\(c = a + b + h \> 0\\). The two other edges at \\(Q\\) have
common differences \\((a + c) - b\\) and \\((b + c) - a\\). Since \\(c =
a + b + h\\) is greater than both \\(a\\)and \\(b\\), these differences
are positive.\\(\\Box\\)

Notice also that this establishes two new triples \\((a, a + b + h, 2 a
+ h)\\) and \\((b, a + b + h, 2 b + h)\\) that continue to point away
from each successive superbase and hence *climb*the topograph. We can
use this lemma (along with a specific form) to show that there are no
cycles in the topograph, i.e. the topograph doesn't loop back on
itself.

Consider the form which takes the following values at a given
superbase:

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/conway_no_cycle.png)](http://www.bossylobster.com/images/blog/conway_no_cycle.png)

</div>

Due to the symmetry, we may consider traveling along an edge in any
direction from this superbase identically. Picking an arbitrary
direction, we reach the following superbase:

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/conway_connected.png)](http://www.bossylobster.com/images/blog/conway_connected.png)

</div>

Since the values must increase indefinitely as laid out by the climbing
lemma, the form can't loop back on itself; if it were to, it would need
to loop back to a smaller value. Since this holds in all directions from
the original well, there are no cycles.

Follow along to [Part
3](http://blog.bossylobster.com/2011/08/conways-topograph-part-3.html).

**Update**: *This material is intentionally aimed at an intermediate
(think college freshman/high school senior) audience. One can go deeper
with it, and I'd love to get more technical off the post.*

**Update**: *All images were created with the
[tikz](http://www.texample.net/tikz/examples/) LaTeX library and can be
compiled with native LaTeX if pgf is installed.*
