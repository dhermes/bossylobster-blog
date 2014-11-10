Title: Finding (Fibonacci) Golden Nuggets Part 1
date: 2011-08-28
author: Danny Hermes (dhermes@bossylobster.com)
tags: Binary Quadratic Form, Conway, Conway's Topograph, Math, Number Theory, Project Euler
slug: finding-fibonacci-golden-nuggets

As I mentioned in my last set ofposts, the content would go somewhere
and this post will be the first to deliver on that. In fact this is the
*all math, no code* first half of a two part post that will deliver. If
you see words like topograph, river, and base and you aren't sure what I
mean, you may want to read that last[set of
posts](http://blog.bossylobster.com/2011/08/conways-topograph-part-3.html).

In this post, I outline a solution to Project Euler [problem
137](http://projecteuler.net/index.php?section=problems&id=137), so stop
reading now if you don't want to be spoiled. There is no code here, but
the [second
half](http://blog.bossylobster.com/2011/08/finding-fibonacci-golden-nuggets-part-2.html)of
this post has a pretty useful abstraction.

The problems asks us to consider \\[A\_F(z) = z F\_1 + z\^2 F\_2 + z\^3
F\_3 + \\ldots,\\] the generating polynomial for the Fibonacci
sequence[\*](http://www.blogger.com/post-edit.g?blogID=1697307561385480651&postID=8793933354039507148#footnote).
The problem defines (without stating so), a sequence
\\(\\left\\{z\_n\\right\\}\_{n \> 0}\\) where \\(A\_F(z\_n) = n\\) and
asks us to find the values \\(n\\) for which \\(z\_n\\) is rational.
Such a value \\(n\\) is called a *golden nugget*.As noted in the
problem statement, \\(A\_F(\\frac{1}{2}) = 2\\), hence \\(z\_2 =
\\frac{1}{2}\\) is rational and \\(2\\) is the first golden nugget.

As a first step, we determine a criterion for \\(n\\) to be a golden
nugget by analyzing the equation \\(A\_F(z) = n\\). With the recurrence
relation given by the Fibonacci sequence as inspiration, we consider
\\begin{align\*}(z + z\^2)A\_F(z) =z\^2 F\_1 &+ z\^3 F\_2 + z\^4 F\_3
+ \\ldots\\\\ &+z\^3 F\_1 + z\^4 F\_2 + z\^5 F\_3 + \\ldots.
\\end{align\*}Due to the fact that \\(F\_2 = F\_1 = 1\\) and the nature
of the recurrence relation, we have \\[(z +z\^2)A\_F(z) = z\^2 F\_2 +
z\^3 F\_3 + z\^4 F\_4 + \\ldots = A\_F(z) -z\\] which implies \\[A\_F(z)
= \\frac{z}{1 - z -z\^2}.\\] Now solving\\(A\_F(z) = n\\), we have
\\[z = n - n z - n z\^2 \\Rightarrow n z\^2 + (n + 1)z - n = 0.\\] In
order for \\(n\\) to be a golden nugget, we must have the solutions
\\(z\\) rational. This only occurs if the discriminant \\[(n + 1)\^2 -
4(n)(-n) = 5 n\^2 + 2 n + 1\\] in the quadratic is the square of a
rational.

So we now positive seek values \\(n\\) such that \\(5 n\^2 + 2 n + 1 =
m\^2\\) for some integer \\(m\\) (the value \\(m\\) must be an integer
since a rational square root of an integer can only be an integer.) This
equation is equivalent to \\[25n\^2 + 10n + 5 = 5m\^2\\] which is
equivalent to \\[5m\^2 - (5 n + 1)\^2 = 4.\\] This is where Conway's
topograph comes in. We'll use the topograph with the quadratic form
\\(f(x, y) = 5 x\^2 - y\^2\\) to find our solutions. First note, a
solution is only valuable if \\(y \\equiv 1 \\bmod{5}\\) since \\(y = 5
n + 1\\) must hold. Also, since \\(\\sqrt{5}\\) is irrational, \\(f\\)
can never take the value \\(0\\), but \\(f(1, 0) = 5\\) and\\(f(0, 1) =
-1\\), hence there is a river on the topograph and the values of \\(f\\)
occur in a periodic fashion.Finally, since we take pairs \\((x, y)\\)
that occur on the topograph, we know \\(x\\) and \\(y\\) share no
factors. Hence solutions \\(f(x, y) = 4\\) can come either come from
pairs on the topograph or by taking a pair which satisfies\\(f(x, y) =
1\\) and scaling up by a factor of \\(2\\) (we will have \\(f(2x, 2y) =
2\^2 \\cdot 1 = 4\\) due to the homogeneity of \\(f\\)).

Starting from the trivial base \\(u = (1, 0)\\) and\\(v = (0, 1)\\),
the full period of the river has length \\(8\\) as seen below:

<div class="separator" style="clear: both; text-align: center;">

[![](http://www.bossylobster.com/images/blog/golden_nugget.png)](http://www.bossylobster.com/images/blog/golden_nugget.png)

</div>

(***Note**: in the above, the values denoted as combinations of \\(u\\)
and \\(v\\) are the vectors for each face on the topograph while the
numbers are the values of \\(f\\) on these vectors.*) Since every edge
protruding from the river on the positive side has a value of \\(4\\) on
a side (the value pairs are \\((5, 4)\\),\\((4, 1)\\),\\((1, 4)\\),
and\\((4, 5)\\)), by the climbing lemma, we know all values above those
on the river have value greater than \\(4\\). Thus, the only solutions
we are concerned with -- \\(f(x, y) = 1\\) or \\(4\\) -- must appear on
the river. Notice on the river, the trivial base \\((u, v)\\) is
replaced by the base \\((9 u + 20 v, 4 u + 9 v)\\). This actually gives
us a concrete recurrence for the river and with it we can get a complete
understanding of our solution set.

When we startfrom the trivial base, we only need consider moving to the
right (orientation provided by the above picture) along the river since
we only care about the absolute value of the coordinates (\\(n\\) comes
from \\(y\\), so it must be positive). As such, we have a sequence of
bases \\(\\left\\{(u\_k, v\_k)\\right\\}\_{k \\geq 0}\\) with \\(u\_0 =
(1, 0)\\),\\(v\_0 = (0, 1)\\) and recurrence \\begin{align\*}u\_{k + 1}
&= 9 u\_k + 20 v\_k \\\\ v\_{k + 1} &= 4 u\_k + 9 v\_k. \\end{align\*}
This implies that both\\(\\left\\{u\_k\\right\\}\\)
and\\(\\left\\{v\_k\\right\\}\\)satisfy the same
relation\\begin{align\*}u\_{k + 2} - 9 u\_{k + 1} - 9(u\_{k + 1} - 9
u\_k) &=20 v\_{k + 1} - 9(20 v\_k) = 20(4 u\_k) \\\\v\_{k + 2} - 9
v\_{k + 1} - 9(v\_{k + 1} - 9 v\_k) &=4 u\_{k + 1} - 9(4 u\_k) = 4(20
v\_k). \\end{align\*} With these recurrences, you can take the three
base solutions on the river and quickly find each successive golden
nugget. Since each value is a coordinate in a vector, it satisfies the
same linear recurrence as the vector. Also, since each of the solution
vectors occur as linear combinations of \\(u\_k\\) and \\(v\_k\\), they
must satisfy the same recurrence as well.

Since the recurrence is degree two, we need the first two values to
determine the entire sequence. For the first solution we start with
\\(u\_0 + v\_0 = (1, 1)\\) and\\(u\_1 + v\_1 = (13, 29)\\); for the
second solution we start with \\(u\_0 + 2 v\_0) = (2, 4)\\) and\\(u\_1
+ 2 v\_1 = (17, 38)\\); andfor the third solution we start with \\(5
u\_0 + 11 v\_0 = (5, 11)\\) and\\(5 u\_1 + 11 v\_1 = (89, 199)\\). For
the second solution, since \\(f(1, 2) = 1\\), we use homogeneity to
scale up to \\((2, 4)\\) and \\((34, 76)\\) to start us off. With these
values, we take the second coordinate along the recurrence and get the
following values:


<center>
<table border="1" style="border-collapse: collapse;">
<tbody>
<tr>
<th>
n

</th>
<th>
First

</th>
<th>
Second

</th>
<th>
Third

</th>
</tr>
<tr>
<td>
0

</td>
<td>
<div style="text-align: center;">

1

</div>

</td>
<td>
<div style="text-align: center;">

4

</div>

</td>
<td>
<div style="text-align: center;">

11

</div>

</td>
</tr>
<tr>
<td>
1

</td>
<td>
<div style="text-align: center;">

29

</div>

</td>
<td>
<div style="text-align: center;">

76

</div>

</td>
<td>
<div style="text-align: center;">

199

</div>

</td>
</tr>
<tr>
<td>
2

</td>
<td>
<div style="text-align: center;">

521

</div>

</td>
<td>
<div style="text-align: center;">

1364

</div>

</td>
<td>
<div style="text-align: center;">

3571

</div>

</td>
</tr>
<tr>
<td>
3

</td>
<td>
<div style="text-align: center;">

9349

</div>

</td>
<td>
<div style="text-align: center;">

24476

</div>

</td>
<td>
<div style="text-align: center;">

64079

</div>

</td>
</tr>
<tr>
<td>
4

</td>
<td>
<div style="text-align: center;">

167761

</div>

</td>
<td>
<div style="text-align: center;">

439204

</div>

</td>
<td>
<div style="text-align: center;">

1149851

</div>

</td>
</tr>
<tr>
<td>
5

</td>
<td>
<div style="text-align: center;">

3010349

</div>

</td>
<td>
<div style="text-align: center;">

7881196

</div>

</td>
<td>
<div style="text-align: center;">

20633239

</div>

</td>
</tr>
<tr>
<td>
6

</td>
<td>
<div style="text-align: center;">

54018521

</div>

</td>
<td>
<div style="text-align: center;">

141422324

</div>

</td>
<td>
<div style="text-align: center;">

370248451

</div>

</td>
</tr>
<tr>
<td>
7

</td>
<td>
<div style="text-align: center;">

969323029

</div>

</td>
<td>
<div style="text-align: center;">

2537720636

</div>

</td>
<td>
<div style="text-align: center;">

6643838879

</div>

</td>
</tr>
<tr>
<td>
8

</td>
<td>
<div style="text-align: center;">

17393796001

</div>

</td>
<td>
<div style="text-align: center;">

45537549124

</div>

</td>
<td>
<div style="text-align: center;">

119218851371

</div>

</td>
</tr>
<tr>
<td>
9

</td>
<td>
<div style="text-align: center;">

312119004989

</div>

</td>
<td>
<div style="text-align: center;">

817138163596

</div>

</td>
<td>
<div style="text-align: center;">

2139295485799

</div>

</td>
</tr>
<tr>
<td>
10

</td>
<td>
<div style="text-align: center;">

5600748293801

</div>

</td>
<td>
<div style="text-align: center;">

14662949395604

</div>

</td>
<td>
<div style="text-align: center;">

38388099893011

</div>

</td>
</tr>
</tbody>
</table>
</center>

We don't get our fifteenth golden nugget candidate (value must be one
more than a multiple of \\(5\\)) until \\(5600748293801\\), which yields
\\(\\boxed{n = 1120149658760}\\). By no means did I do this by hand in
real life; I didn't make a pretty representation of the river either. I
just wanted to make the idea clear without any code. To get to the code
(and the way you should approach this stuff), move on to the[second
half](http://blog.bossylobster.com/2011/08/finding-fibonacci-golden-nuggets-part-2.html)
of this post.


<div id="footnote">

*\*The Fibonacci sequence is given by \\(F\_0 = 0\\),\\(F\_1 =
1\\),and\\(F\_{n} =F\_{n - 1} +F\_{n - 2}\\).*

</div>
