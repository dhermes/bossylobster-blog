Title: Trigonometry and Nested Radicals
date: 2013-11-25
author: Danny Hermes (dhermes@bossylobster.com)
tags: Approximation, Infinite Nested Radical, Math, Nested Radical, Pi, Radical, Root Two, Square Root
slug: trigonometry-and-nested-radicals

Early last month, I was chatting with one of my officemates about a
curious problem I had studied in high school. I hadn't written any of
the results down, so much of the discussion involved me rediscovering
the results and proving them with much more powerful tools than I once
possessed.  
  
Before writing about the problem I had played around with, I want to
give a ~~brief~~ motivation. For as long as humans have been doing
mathematics, finding values of \\(\\pi\\) has been deemed worthwhile (or
every generation has just found it worthwhile to waste time computing
digits).  
  
One such way the Greeks (particularly
[Archmides](http://www.math.utah.edu/~alfeld/Archimedes/Archimedes.html))
computed \\(\\pi\\) was by approximating a circle by a regular polygon
and letting the number of sides grow large enough so that the error
between the area of the unit circle (\\(\\pi \\cdot 1\^2\\)) and the
area of the polygon would be smaller than some fixed threshold. Usually
these thresholds were picked to ensure that the first \\(k\\) digits
were fully accurate (for some appropriate value of \\(k\\)).  
  
In many introductory Calculus courses, this problem is introduced
exactly when the limit is introduced and students are forced to think
about the [area problem](http://www.qbyte.org/puzzles/p045s.html) in the
regular polygon:  

<div class="separator" style="clear: both; text-align: center;">

[![](http://1.bp.blogspot.com/-VRz8LKn081A/UpPU9TzebwI/AAAAAAAANJs/qK36fAX2aOY/s1600/p045.png "From http://www.qbyte.org/puzzles/p045s.html")](http://1.bp.blogspot.com/-VRz8LKn081A/UpPU9TzebwI/AAAAAAAANJs/qK36fAX2aOY/s1600/p045.png)

</div>

<div class="separator" style="clear: both; text-align: center;">

</div>

Given \\(N\\) sides, the area is \\(N \\cdot T\_N\\) where \\(T\_N\\) is
the area of each individual triangle given by one side of the polygon
and the circumcenter.  
  
Call one such triangle \\(\\Delta ABC\\) and let \\(BC\\) be the side
that is also a side of the polygon while the other sides have
\\(\\left|AB\\right| = \\left|AC\\right| = 1\\) since the polygon is
inscribed in a unit circle. The angle \\(\\angle BAC =
\\frac{2\\pi}{N}\\) since each of the triangles has the same internal
angle and there are \\(N\\) of them. If we can find the perpendicular
height \\(h\\) from \\(AB\\) to \\(C\\), the area will be
\\(\\frac{1}{2} h \\left|AB\\right| = \\frac{h}{2}\\). But we also know
that  
\\[\\sin\\left(\\angle BAC\\right) = \\frac{h}{\\left|AC\\right|}
\\Rightarrow h = \\sin\\left(\\frac{2\\pi}{N}\\right).\\] Combining all
of these, we can approximate \\(\\pi\\) with the area:  
\\[\\pi \\approx \\frac{N}{2} \\sin\\left(\\frac{2\\pi}{N}\\right) =
\\pi \\frac{\\sin\\left(\\frac{2\\pi}{N}\\right)}{\\frac{2 \\pi}{N}}.
\\] As I've shown my [Math
1A](http://math.berkeley.edu/courses/choosing/lowerdivcourses/math1A)
students, we see that  
\\[\\lim\_{N \\to \\infty} \\pi
\\frac{\\sin\\left(\\frac{2\\pi}{N}\\right)}{\\frac{2 \\pi}{N}} = \\pi
\\lim\_{x \\to 0} \\frac{\\sin(x)}{x} = \\pi\\] so these are indeed good
approximations.  

### Theory is Nice, But I Thought We Were Computing Something

Unfortunately for us (and Archimedes), computing
\\(\\sin\\left(\\frac{2\\pi}{N}\\right)\\) is not quite as simple as
dividing by \\(N\\), so often special values of \\(N\\) were chosen. In
fact, starting from \\(N\\) and then using \\(2N\\), the areas could be
computed via a special way of averaging the previous areas. Lucky for
us, such a method is equivalent to the trusty [half angle
identities](http://en.wikipedia.org/wiki/List_of_trigonometric_identities#Double-angle.2C_triple-angle.2C_and_half-angle_formulae) (courtesy
of [Abraham De Moivre](http://en.wikipedia.org/wiki/Abraham_de_Moivre)).
To keep track of these polygons with a power of two as the number of
sides, we call \\(A\_n = \\frac{2\^n}{2}
\\sin\\left(\\frac{2\\pi}{2\^n}\\right)\\).  
  
Starting out with the simplest polygon, the square with \\(N = 2\^2\\)
sides, we have  
\\[A\_2 = 2 \\sin\\left(\\frac{\\pi}{2}\\right) = 2.\\] Jumping to the
[octagon](http://en.wikipedia.org/wiki/Octagon) (no not that "[The
Octagon](https://www.google.com/search?q=%22the+octagon%22&tbm=isch)"),
we have  
\\[A\_3 = 4 \\sin\\left(\\frac{\\pi}{4}\\right) = 4 \\frac{\\sqrt{2}}{2}
= 2 \\sqrt{2}.\\] So far, the toughest thing we've had to deal with is a
\\(45\^{\\circ}\\) angle and haven't yet had to lean on Abraham
([him](http://www.nocturnar.com/imagenes/abraham-de-moivre-mathematician-abraham-de-moivre.jpg), [not
him](http://foglobe.com/data_images/main/abraham-lincoln/abraham-lincoln-03.jpg)) for
help. The [hexadecagon](http://en.wikipedia.org/wiki/Hexadecagon) wants
to change that:  
\\[A\_4 = 8 \\sin\\left(\\frac{\\pi}{8}\\right) = 8 \\sqrt{\\frac{1 -
\\cos\\left(\\frac{\\pi}{4}\\right)}{2}} = 8 \\sqrt{\\frac{2 -
\\sqrt{2}}{4}} = 4 \\sqrt{2 - \\sqrt{2}}.\\]

<div>

To really drill home the point (and motivate my next post) we'll compute
this for the \\(32\\)-gon (past the point where polygons have worthwhile
names):

</div>

<div>

\\[A\_5 = 16 \\sin\\left(\\frac{\\pi}{16}\\right) = 16 \\sqrt{\\frac{1 -
\\cos\\left(\\frac{\\pi}{8}\\right)}{2}}.\\] Before, we could rely on
the fact that we know that a \\(45-45-90\\) triangle looked like, but
now, we come across \\(\\cos\\left(\\frac{\\pi}{8}\\right)\\), a value
which we haven't seen before. Luckily, Abraham has help here as well:  
\\[\\cos\\left(\\frac{\\pi}{8}\\right) = \\sqrt{\\frac{1 +
\\cos\\left(\\frac{\\pi}{4}\\right)}{2}} = \\sqrt{\\frac{2 +
\\sqrt{2}}{4}} = \\frac{1}{2} \\sqrt{2 + \\sqrt{2}}\\] which lets us
compute  
\\[A\_5 = 16 \\sqrt{\\frac{1 - \\frac{1}{2} \\sqrt{2 + \\sqrt{2}}}{2}} =
8 \\sqrt{2 - \\sqrt{2 + \\sqrt{2}}}.\\]

</div>

<div>

  

</div>

<div>

So why have I put you through all this? If we wave our hands like a
[magician](http://imgs.tuts.dragoart.com/how-to-draw-fantasia-wizard-mickey_1_000000008546_5.jpg),
we can see this pattern continues and for the general \\(n\\)

</div>

<div>

\\[A\_n = 2\^{n - 2} \\sqrt{2 - \\sqrt{2 + \\sqrt{2 + \\sqrt{\\cdots +
\\sqrt{2}}}}}\\]

</div>

<div>

where there are \\(n - 3\\) nested radicals with the \\(\\oplus\\) sign
and only one minus sign at the beginning.

</div>

<div>

  

</div>

<div>

This motivates us to study two questions, what is the limiting behavior
of such a nested radical:

</div>

\\[\\sqrt{2 + s\_1 \\sqrt{2 + s\_2 \\sqrt{ \\cdots }}}\\] as the signs
\\(s\_1, s\_2, \\ldots\\) takes values in \\(\\left\\{-1,
1\\right\\}\\). Recasting in terms of the discussion above, we want to
know how close we are to \\(\\pi\\) as we increase the number of sides.

<div>

  

</div>

<div>

When I was in high school, I just loved to [nerd
out](http://blog.verdebmx.com/wp-content/uploads/2008/07/computer.jpg) on
any and all math problems, so I studied this just for fun. Having heard
about the unfathomable brain of
[Ramanujan](http://en.wikipedia.org/wiki/Srinivasa_Ramanujan) and the
fun [work he had done](http://www.isibang.ac.in/~sury/ramanujanday.pdf)
with infinitely [nested
radicals](http://en.wikipedia.org/wiki/Nested_radical), I wanted to
examine which sequences of signs \\((s\_1, s\_2, \\ldots)\\) produced an
infinite radical that converged and what the convergence behavior was.

</div>

<div>

  

</div>

<div>

I'm fairly certain my original questions came from an Illinois Council
of Teachers of Mathematics ([ICTM](http://www.ictm.org/contest.html))
contest problem along the lines of

</div>

<div>

\\[\\text{Find the value of the infinite nested radical } \\sqrt{2 +
\\sqrt{2 + \\cdots}}\\] or maybe the slightly more difficult
\\[\\text{Find the value of the infinite nested radical } \\sqrt{2 -
\\sqrt{2 + \\sqrt{2 - \\sqrt{2 + \\cdots}}}}.\\]
[Armed](http://www.search-best-cartoon.com/cartoon-moose/armed-cartoon-moose.jpg)
with my
[TI-83](http://img1.targetimg1.com/wcsstore/TargetSAS//img/p/93/50/93505.jpg),
I set out to do some hardcore programming and figure it out. It took me
around a month of off-and-on tinkering. This second time around as a
mathematical grown-up, it took me the first half of a plane ride from
SFO to Dallas.

</div>

<div>

  

</div>

<div>

In the next few weeks/months, I hope to write a few blog posts,
including math, proofs and some real code on what answers I came up with
and what other questions I have.

</div>

[About Bossy Lobster](https://profiles.google.com/114760865724135687241)

</p>

