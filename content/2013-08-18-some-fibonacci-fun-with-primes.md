Title: Some Fibonacci Fun with Primes
date: 2013-08-18
author: Danny Hermes (dhermes@bossylobster.com)
tags: Algebra, Fibonacci, Finite Field, Linear Algebra, Math, Number Theory
slug: some-fibonacci-fun-with-primes

I haven't written in way too long and just wanted to post this fun
little proof.

**Assertion:** Let \\(F\_n\\) be the \\(n\\)th Fibonacci number defined
by \\(F\_n = F\_{n-1} + F\_{n-2}\\), \\(F\_0 = 0, F\_1 = 1\\). Show that
for an odd prime \\(p\\neq 5\\), we have \\(p\\) divides
\\(F\_{p\^2-1}\\).

**Proof:** We do this by working inside \\(\\mathbb{F}\_p\\) instead of
working in \\(\\mathbb{R}\\). The recurrence is given by

\\[ \\left( \\begin{array}{cc}
1 & 1 \\\\
1 & 0 \\end{array} \\right)
\\left( \\begin{array}{c}
F\_{n-1} \\\\
F\_{n-2} \\end{array} \\right)
=
\\left( \\begin{array}{c}
F\_{n-1} + F\_{n-2} \\\\
F\_{n-1} \\end{array} \\right)
=
\\left( \\begin{array}{c}
F\_n \\\\
F\_{n-1} \\end{array} \\right)\\] and in general
\\[ \\left( \\begin{array}{cc}
1 & 1 \\\\
1 & 0 \\end{array} \\right)\^{n}
\\left( \\begin{array}{c}
1 \\\\
0 \\end{array} \\right)
=
\\left( \\begin{array}{cc}
1 & 1 \\\\
1 & 0 \\end{array} \\right)\^{n}
\\left( \\begin{array}{c}
F\_1 \\\\
F\_0 \\end{array} \\right)
=
\\left( \\begin{array}{c}
F\_{n + 1} \\\\
F\_n \\end{array} \\right)\\] The matrix \\(A =
\\left(\\begin{array}{cc} 1 & 1 \\\\ 1 & 0 \\end{array} \\right)\\) has
characteristic polynomial
\\[\\chi\_A(t) = (1 - t)(0 - t) - (1)(1) = t\^2 - t - 1\\] If this
polynomial has distinct roots, then \\(A\\) is diagonalizable (this is
sufficient, but not necessary). Assuming the converse we have
\\(\\chi\_A(t) = (t - \\alpha)\^2\\) for some \\(\\alpha \\in
\\mathbb{F}\_p\\); we can assume \\(\\alpha \\in \\mathbb{F}\_p\\) since
\\(-2\\alpha = -1\\) is the coefficient of \\(t\\), which means
\\(\\alpha = 2\^{-1} \\) (we are fine with this since \\(p\\) odd means
that \\(2\^{-1}\\) exists). In order for this to be a root of
\\(\\chi\_A\\), we must have
\\[0 \\equiv 4 \\cdot \\chi\_A\\left(2\^{-1}\\right) \\equiv 4 \\cdot
\\left(2\^{-2} - 2\^{-1} - 1\\right) \\equiv 1 - 2 - 4 \\equiv -5
\\bmod{p}.\\] Since \\(p \\neq 5\\) is prime, this is not possible,
hence we reached a contradiction and \\(\\chi\_A\\) does not have a
repeated root.

Thus we may write \\(\\chi\_A(t) = (t - \\alpha)(t - \\beta)\\) for
\\(\\alpha, \\beta \\in \\mathbb{F}\_{p\^2}\\) (it's possible that
\\(\\chi\_A\\) is irreducible over \\(\\mathbb{F}\_p\\), but due to
degree considerations it **must** split completely over
\\(\\mathbb{F}\_{p\^2}\\)). Using this, we may write

\\[A = P \\left(\\begin{array}{cc} \\alpha & 0 \\\\ 0 & \\beta
\\end{array} \\right) P\^{-1}\\] for some \\(P \\in GL\_{2}
\\left(\\mathbb{F}\_{p\^2}\\right)\\) and so

\\[A\^{p\^2 - 1} = P \\left(\\begin{array}{cc} \\alpha & 0 \\\\ 0 &
\\beta \\end{array} \\right)\^{p\^2 - 1} P\^{-1}
= P \\left(\\begin{array}{cc} \\alpha\^{p\^2 - 1} & 0 \\\\ 0 &
\\beta\^{p\^2 - 1} \\end{array} \\right)P\^{-1}\\] Since \\(\\chi\_A(0)
= 0 - 0 - 1 \\neq 0\\) we know \\(\\alpha\\) and \\(\\beta\\) are
nonzero, hence \\(\\alpha\^{p\^2 - 1} = \\beta\^{p\^2 - 1} = 1 \\in
\\mathbb{F}\_{p\^2} \\). Thus \\(A\^{p\^2 - 1} = P I\_2 P\^{-1} =
I\_2\\) and so

\\[\\left( \\begin{array}{c}
F\_p \\\\
F\_{p\^2 - 1} \\end{array} \\right)
=
\\left( \\begin{array}{cc}
1 & 1 \\\\
1 & 0 \\end{array} \\right)\^{p\^2 - 1}
\\left( \\begin{array}{c}
1 \\\\
0 \\end{array} \\right)
=
I\_2 \\left( \\begin{array}{c}
1 \\\\
0 \\end{array} \\right)
=
\\left( \\begin{array}{c}
1 \\\\
0 \\end{array} \\right)\\] so we have \\(F\_{p\^2 - 1} = 0\\) in
\\(\\mathbb{F}\_p\\) as desired.

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
