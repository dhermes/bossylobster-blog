Title: Continued fraction expansions of irrational square roots
date: 2011-07-18
author: Danny Hermes (dhermes@bossylobster.com)
tags: Algebra, Continued Fractions, Math, Quadratic Irrational, Square Root
slug: continued-fraction-expansions-of

I had no idea (until this Thursday, July 16) that I had never seen a
proof of the fact that the continued fraction expansion of
\\(\\sqrt{D}\\) is periodic whenever \\(D\\) is not a perfect square.
But have no fear, I found out about something called a *reduced
quadratic irrational* and now have a proof. Here we go.

**Definition**:An irrational root \\(\\alpha\\) of a quadratic equation
with integer coefficients is called *reduced* if \\(\\alpha \> 1\\) and
its conjugate\\(\\tilde{\\alpha}\\) satisfies \\(-1 \< \\tilde{\\alpha}
\< 0\\).\\(\\Box\\)

Solutions (since assumed real) of such quadratics can be written
as\$\$\\alpha = \\frac{\\sqrt{D} + P}{Q}\$\$ where \\(D, P, Q \\in
\\mathbf{Z}\\) and \\(D, Q \> 0\\). It is also possible (though not
required) to ensure that \\(Q\\) divides \\(D - P\^2\\). This is
actually a necessary assumption for some of the stuff I do, is
mentioned[here](http://en.wikipedia.org/wiki/Periodic_continued_fraction#Relation_to_quadratic_irrationals)and
generally frustrated the heck out of me, so that. As an example for some
enlightenment, notice \$\$\\alpha = \\frac{2 + \\sqrt{7}}{4}\$\$ is
reduced but \\(4\\) does not divide \\(7 - 2\^2\\). However, if we write
this as \\(\\frac{8 + \\sqrt{112}}{16}\\), we have our desired
condition.

**Definition**: We say a reduced quadratic irrational \\(\\alpha\\) is
*associated* to \\(D\\) if we can write \$\$\\alpha = \\frac{P +
\\sqrt{D}}{Q}\$\$ and \\(Q\\) divides \\(D - P\^2\\).\\(\\Box\\)
**
**
**Lemma 1**: Transforming a reduced irrational root \\(\\alpha\\)
associated to \\(D\\) into its integer part and fractional partvia
\$\$\\alpha = \\lfloor \\alpha \\rfloor + \\frac{1}{\\alpha'},\$\$ the
resulting quadratic irrational \\(\\alpha'\\) is reduced andassociated
to \\(D\\)as well.(This is what one does during continued fraction
expansion, and as I did with \\(\\sqrt{2}\\) during my[last
post](http://blog.bossylobster.com/2011/07/continued-fractions-for-greater-good.html).)

**Proof**: Letting \$\$\\alpha = \\frac{\\sqrt{D} + P}{Q}\$\$ and \\(X
=\\lfloor \\alpha \\rfloor\\), we have \$\$\\frac{1}{\\alpha'} =
\\frac{\\sqrt{D} - (QX - P)}{Q}.\$\$


-   Since \\(\\sqrt{D}\\) is irrational, we must have
    \\(\\frac{1}{\\alpha'} \> 0\\) and since \\(\\frac{1}{\\alpha'}\\)
    is the fractional part we know \$\$0 \<\\frac{1}{\\alpha'} \< 1
    \\Rightarrow\\alpha' \> 1.\$\$
-   Transforming \$\$\\alpha' = \\frac{Q}{\\sqrt{D} - (QX - P)}
    \\cdot\\frac{\\sqrt{D} + (QX - P)}{\\sqrt{D} + (QX - P)}
    =\\frac{\\sqrt{D} + (QX - P)}{\\frac{1}{Q}\\left(D - (QX -
    P)\^2\\right)},\$\$ we have \\(P' = QX - P\\) and\\(Q'
    =\\frac{1}{Q}\\left(D - (QX - P)\^2\\right)\\) and need to show
    \\(Q' \\in \\mathbf{Z}\\).But \\(D - (QX - P)\^2 \\equiv D - P\^2
    \\bmod{Q}\\) and since \\(\\alpha\\) is associated to \\(D\\),
    \\(Q\\) must divide this quantity, hence \\(Q'\\) is an integer.
-   Since \\(X = \\lfloor\\frac{\\sqrt{D} + P}{Q}\\rfloor\\) is an
    integer and \\(\\alpha\\) is irrational, we know\\(X \<
    \\frac{\\sqrt{D} + P}{Q}\\) hence \\(P' = QX - P \< \\sqrt{D}\\)
    forcing \\(\\tilde{\\alpha}' \< 0\\).
-   Since \\(\\alpha \> 1\\) we know \\(X \\geq 1 \\Leftrightarrow 0
    \\leq X - 1\\). Thus \\begin{align\*}\\tilde{\\alpha} = \\frac{P -
    \\sqrt{D}}{Q} &\< 0 \\leq X - 1 \\\\ \\Rightarrow Q &\< \\sqrt{D} +
    (QX - P) \\\\\\Rightarrow Q(\\sqrt{D} - (QX - P))&\< D - (QX -
    P)\^2 \\\\\\Rightarrow -\\tilde{\\alpha}' = \\frac{\\sqrt{D} - (QX
    - P)}{\\frac{1}{Q}\\left(D - (QX - P)\^2\\right)} &\<
    1\\end{align\*} hence \\(\\tilde{\\alpha}' \> -1\\) and
    \\(\\alpha'\\) is reduced.
-   Since\\(Q' =\\frac{1}{Q}\\left(D - (P')\^2\\right)\\), we know
    \$\$D - (P')\^2 \\equiv Q Q' \\equiv 0 \\bmod{Q'}\$\$ hence
    \\(\\alpha'\\) is associated to \\(D\\).


**<span class="Apple-style-span" style="font-weight: normal;">Thus
\\(\\alpha'\\) is both reduced and associated to \\(D\\).
\\(\\Box\\)</span>**
**
**
**Lemma 2**: There are finitely many reduced quadratic irrationals
associated to a fixed \\(D\\).

**Proof**: As above write an arbitrary reduced irrational as \\(\\alpha
= \\frac{\\sqrt{D} + P}{Q}\\). Since \\(\\alpha \> 1\\)
and\\(\\tilde{\\alpha} \> -1\\), we know \\(\\alpha + \\tilde{\\alpha}
= \\frac{2P}{Q} \> 0\\) hence with the assumption \\(Q \> 0\\) we have
\\(P \> 0\\). Since \\(\\tilde{\\alpha} \< 0\\) we also have \\(P \<
\\sqrt{D}\\). Also, since \\(\\alpha \> 1\\) by assumption we have \\(Q
\< P + \\sqrt{D} \< 2\\sqrt{D}\\) thus there are finitely many choices
for both \\(P\\) and \\(Q\\), forcing finitely many reduced quadratic
irrationals associated to a fixed \\(D\\) (this amount is strictly
bounded above by \\(2D\\)). \\(\\Box\\)

**Claim**:The continued fraction expansion of \\(\\sqrt{D}\\) is
periodic whenever \\(D\\) is not a perfect square.

**Proof**: We'll use Lemma 1 to establish a series of reduced quadratic
irrationals associated to \\(D\\) and then use Lemma 2 to assert this
series must repeat (hence be periodic) due to the finite number of such
irrationals.

Write \\(a\_0 = \\lfloor \\sqrt{D} \\rfloor\\) and \\(\\sqrt{D} = a\_0 +
\\frac{1}{\\alpha\_0}\\). From here, we will prove


-   \\(\\alpha\_0\\) is a reduced quadratic irrational associated to
    \\(D\\).
-   By defining \\(a\_{i+1} = \\lfloor \\alpha\_i \\rfloor\\) and
    \\(\\alpha\_i = a\_{i + 1} + \\frac{1}{\\alpha\_{i +
    1}}\\),\\(\\alpha\_{i + 1}\\) is also a reduced quadratic
    irrational associated to \\(D\\) (assuming all \\(\\alpha\\) up
    until \\(i\\) are as well).



Since \\(\\frac{1}{\\alpha\_0}\\) is the fractional part of the
irrational \\(\\sqrt{D}\\), we have\$\$0 \< \\frac{1}{\\alpha\_0} \< 1
\\Rightarrow \\alpha\_0 \> 1.\$\$By simple algebra, we have
\$\$\\alpha\_0 = \\frac{a\_0 + \\sqrt{D}}{D - a\_0\^2}, \\qquad
\\tilde{\\alpha\_0} = \\frac{a\_0 - \\sqrt{D}}{D - a\_0\^2}.\$\$ Since
\\(a\_0\\) is the floor, we know \\(a\_0 - \\sqrt{D} \< 0
\\Rightarrow\\tilde{\\alpha\_0} \< 0\\). Since \\(D \\in \\mathbf{Z}
\\Rightarrow \\sqrt{D} \> 1\\) and \\(\\sqrt{D} \> a\_0\\), we have
\$\$1 \< \\sqrt{D} + a\_0 \\Rightarrow\\sqrt{D} - a\_0 \< D -
a\_0\^2\\Rightarrow a\_0 - \\sqrt{D} \> -(D - a\_0\^2)\\Rightarrow
\\tilde{\\alpha\_0} \> -1.\$\$ Thus \\(\\alpha\_0\\) is a reduced
quadratic irrational. Since \\(P\_0 = a\_0\\) and \\(Q\_0 = D - a\_0\^2
= D - P\_0\^2\\), \\(Q\_0\\) clearly divides \\(D - P\_0\^2\\) so
\\(\\alpha\_0\\) is associated to \\(D\\) as well.

Following the recurrence defined, since each \\(\\alpha\_i\\) is a
reduced quadratic irrational, each \\(a\_i \\geq 1\\). Also, by Lemma 1,
each \\(\\alpha\_{i + 1}\\) is reduced and associated to \\(D\\) since
\\(\\alpha\_0\\) is. By Lemma 2, we only have finitely many choices for
these, hence there must be some smallest \\(k\\) for which \\(\\alpha\_k
= \\alpha\_0\\). Since \\(\\alpha\_{i + 1}\\) is determined completely
by \\(\\alpha\_i\\) we will then have \\(\\alpha\_{k + j} =
\\alpha\_j\\) for all \\(j \> 0\\), hence the \\(\\alpha\_i\\) are
periodic. Similarly, as the \\(a\_i\\) for \\(i \> 0\\) are determined
completely by \\(\\alpha\_{i - 1}\\), the \\(a\_i\\) must be periodic as
well, forcing the continued fraction expansion \$\$\\sqrt{D} = a\_0 +
\\cfrac{1}{a\_1 +\\cfrac{1}{a\_2 +\\ddots}}\$\$ to be
periodic.\\(\\Box\\)

**Update:** I
[posted this](http://www.proofwiki.org/wiki/Continued_Fraction_Expansion_of_Irrational_Square_Root)
on

<div markdown="1" style="text-align: center;">
  ![ProofWiki logo](/images/175px-Logo.png)
</div>

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
