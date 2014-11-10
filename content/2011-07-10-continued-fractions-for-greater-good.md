Title: Continued Fractions for the Greater Good part 1
date: 2011-07-10
author: Danny Hermes (dhermes@bossylobster.com)
tags: Algebra, Continued, Fractions, Math
slug: continued-fractions-for-greater-good

OK, maybe not for the greater good, but still fun. This first post will
be relatively short and sweet, intended to give an introduction for the
posts that will follow.

Before the introduction, some
[motivation](http://en.wikipedia.org/wiki/Continued_fraction#Motivation)
courtesy of [Wikipedia](http://en.wikipedia.org/wiki/Main_Page):

<div>

> "...decimal representation has some problems. One problem is that many
> rational numbers lack finite representations in this system. For
> example, the number \\(\\frac{1}{3}\\) is represented by the infinite
> sequence \\((0, 3, 3, 3, 3, \\ldots )\\). Another problem is that the
> constant \\(10\\) is an essentially arbitrary choice, and one which
> biases the resulting representation toward numbers that have some
> relation to the integer \\(10\\). For example, \\(\\frac{137}{1600}\\)
> has a finite decimal representation, while \\(\\frac{1}{3}\\) does
> not, not because \\(\\frac{137}{1600}\\)is simpler than
> \\(\\frac{1}{3}\\), but because \\(1600\\)happens to divide a power
> of \\(10\\) (\\(10\^6 = 1600 \\times 625\\)). Continued fraction
> notation is a representation of the real numbers that avoids both
> these problems.Let us consider how we might describe a number like
> \\(\\frac{415}{93}\\), which is around \\(4.4624\\). This is
> approximately \\(4\\). Actually it is a little bit more than\\(4\\),
> about\\(4 + \\frac{1}{2}\\). But the\\(2\\)in the denominator is
> not correct; the correct denominator is a little bit more
> than\\(2\\) about\\(2 + \\frac{1}{6}\\),
> so\\(\\frac{415}{93}\\)is approximately\$\$4 +
> \\cfrac{1}{2+\\cfrac{1}{6}}.\$\$ But the \\(6\\) in the denominator is
> not correct; the correct denominator is a little bit more than
> \\(6\\), actually \\(6+\\frac{1}{7}\\). So \\(\\frac{415}{93}\\) is
> actually\$\$4 + \\cfrac{1}{2+\\cfrac{1}{6 +\\cfrac{1}{7}}}.\$\$This
> is exact..."

With this in mind, one can define an infinite continued fraction to be
\$\$a\_0 + \\cfrac{1}{a\_1 +\\cfrac{1}{a\_2 +\\ddots}}.\$\$ With the
denominators \\(a\_0, a\_1, a\_2, \\ldots\\), we can define a recurrence
for the finite approximations (convergents) of this value. For example,
the zeroth is \\(a\_0\\) and the first is \\(a\_0 + \\frac{1}{a\_1} =
\\frac{a\_0 a\_1 + 1}{a\_1}\\).

The other motivation (the one I actually learned first in real life) for
continued fractions comes from \\(\\sqrt{2}\\) being represented by an
infinite continued fraction. (Instead of saying a probability of
\\(0.01876\\), people would rather say a \\(1\\) in \\(53\\) chance.) So
we try to write \\(\\sqrt{2} = 1.41421356\\ldots\\) as \\(1 +
\\frac{1}{2.414}\\). But, instead, notice that \$\$\\sqrt{2} = 1 +
(\\sqrt{2} - 1) = 1 + \\frac{1}{\\sqrt{2} + 1}.\$\$ Plugging this into
itself, we have\$\$\\sqrt{2} = 1 + \\cfrac{1}{1 +1 +
\\cfrac{1}{\\sqrt{2} + 1}} =1 + \\cfrac{1}{1 +1 + \\cfrac{1}{1 + 1 +
\\cfrac{1}{\\sqrt{2} + 1}}}\$\$ and notice it can be represented by
\\((1; 2, 2, 2, \\ldots)\\).

Define the \\(n\\)th convergent to be \\(\\frac{h\_n}{k\_n}\\), so above
we have \\(h\_0 = a\_0, k\_0 = 1\\) and\\(h\_1 = a\_0 a\_1 + 1, k\_0 =
a\_1\\).

Claim:\\(h\_n\\) and \\(k\_n\\) satisfy \\begin{align\*}h\_n &= a\_n
h\_{n - 1} + h\_{n - 2} \\\\k\_n &= a\_n k\_{n - 1} + k\_{n -
2}\\end{align\*}along with \\(h\_{-1} = 1, h\_{-2} = 0\\) and
\\(k\_{-1} = 0, k\_{-2} = 1\\).

Proof: The fraction \\(\\frac{h\_n}{k\_n}\\) is converted
into\\(\\frac{h\_{n + 1}}{k\_{n + 1}}\\) simply by changing \\(a\_n\\)
to \\(a\_n + \\frac{1}{a\_{n + 1}}\\) in the final denominator.
Since\$\$\\frac{h\_n}{k\_n} = \\frac{a\_n h\_{n - 1} + h\_{n - 2}}{a\_n
k\_{n - 1} + k\_{n - 2}}\$\$ we similarly have
\\begin{align\*}\\frac{h\_{n + 1}}{k\_{n + 1}} &= \\frac{\\left(a\_n +
\\frac{1}{a\_{n + 1}}\\right)h\_{n - 1} + h\_{n - 2}}{\\left(a\_n +
\\frac{1}{a\_{n + 1}}\\right)k\_{n - 1} + k\_{n - 2}} \\\\ &=
\\frac{a\_{n + 1}(a\_n h\_{n - 1} + h\_{n - 2}) + h\_{n - 1}}{a\_{n +
1}(a\_n k\_{n - 1} + k\_{n - 2}) + k\_{n - 1}} \\\\&= \\frac{a\_{n + 1}
h\_n + h\_{n - 1}}{a\_{n + 1} k\_n + k\_{n - 1}}\\end{align\*}
Thus \\(h\_{n + 1}\\) and \\(k\_{n + 1}\\) satisfy the same recurrence.

It remains to check the initial conditions work, but note
\\begin{align\*}h\_0 &= a\_0 h\_{-1} + h\_{-2} = a\_0 \\cdot 1 + 0 =
a\_0 \\\\k\_0 &= a\_0 k\_{-1} + k\_{-2} = a\_0 \\cdot 0 + 1 =
1\\end{align\*} and\\begin{align\*}h\_1 &= a\_1 h\_{0} + h\_{-1} = a\_0
a\_1 + 1 \\\\k\_1 &= a\_1 k\_{0} + k\_{-1} = a\_1 \\cdot 1 + 0 =
a\_1\\end{align\*} as we checked above. \\(\\Box\\)

Check out my[next
post](http://blog.bossylobster.com/2011/07/continued-fraction-expansions-of.html),
where I actually accomplish something with fractions (or at least
prepare to accomplish something).

</div>
