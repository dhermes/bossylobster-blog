Title: Calculating a Greatest Common Divisor with Dirichlet's Help
date: 2013-09-10
author: Danny Hermes (dhermes@bossylobster.com)
tags: Dirichlet, Math, Mathematics, Number Theory, Prime Number
slug: calculating-greatest-common-divisor

Having just left Google and started my PhD in Applied Mathematics
at [Berkeley](http://math.berkeley.edu/), I thought it might be
appropriate to write some (more) math-related blog posts. Many of these
posts, I jotted down on napkins and various other places on the web and
just haven't had time to post until now.

For today, I'm posting a result which was somewhat fun to figure out
with/for one of
my [buddies](https://picasaweb.google.com/101796704659729637490/WhereHasYourMathTShirtBeen#5802889644579484306) from
[Michigan Math](http://www.lsa.umich.edu/math/). I'd also like to point
out that he is absolutely kicking ass at Brown.

While trying to determine if
\\[J(B\_n)\_{\\text{Tor}}\\left(\\mathbb{Q}\\right) \\stackrel{?}{=}
\\mathbb{Z}/2\\mathbb{Z} \\] where \\(J(B\_n)\\) is the Jacobian of the
curve \\(B\_n\\) given by \\(y\^2 = (x + 2) \\cdot f\^n(x)\\) where
\\(f\^n\\) denotes \\(\\underbrace{f \\circ \\cdots \\circ f}\_{n
\\text{ times}}\\) and \\(f(x) = x\^2 - 2\\).

Now, his and my interests diverged some time ago, so I can't appreciate
what steps took him from this to the problem I got to help with.
However, he was able to show (trivially maybe?) that this was equivalent
to showing that
\\[\\gcd\\left(5\^{2\^n} + 1, 13\^{2\^n} + 1, \\ldots, p\^{2\^n} + 1,
\\ldots \\right) = 2 \\qquad (1)\\] where the \\(n\\) in the exponents
is the same as that in \\(B\_n\\) and where the values we are using in
our greatest common divisor (e.g. \\(5, 13\\) and \\(p\\) above) are all
of the primes \\(p \\equiv 5 \\bmod{8}\\).

My buddy, being sadistic and for some reason angry with me, passed me
along the stronger statement:
\\[\\gcd\\left(5\^{2\^n} + 1, 13\^{2\^n} + 1\\right) = 2 \\qquad (2)\\]
which I of course struggled with and tried to beat down with tricks like
\\(5\^2 + 12\^2 = 13\^2\\). After a few days of this struggle, he
confessed that he was trying to ruin my life and told me about the
weaker version \\((1)\\).

When he sent me the email informing me of this, I read it at 8am, drove
down to Santa Clara for [PyCon](https://us.pycon.org/2013/) and by the
time I arrived at 8:45am I had figured the weaker case \\((1)\\) out.
This felt much better than the days of struggle and made me want to
write about my victory (which I'm doing now). Though, before we actually
demonstrate the weaker fact \\((1)\\)  I will admit that I am not in
fact tall. Instead I stood on the shoulders of Dirichlet and [called
myself tall](http://www.youtube.com/watch?v=A6f-6l0W-0o#t=35s).
Everything else is bookkeeping.

<span style="font-size: large;">Let's Start the Math</span>
-----------------------------------------------------------

First, if \\(n = 0\\), we see trivially that
\\[\\gcd\\left(5\^{2\^0} + 1, 13\^{2\^0} + 1\\right) = \\gcd\\left(6,
14\\right) = 2\\] and all the remaining terms are divisible by \\(2\\)
hence the \\(\\gcd\\) over all the primes must be \\(2\\).

Now, if \\(n \> 0\\), we will show that \\(2\\) divides our \\(\\gcd\\),
but \\(4\\) does not and that no odd prime can divide this \\(\\gcd\\).
First, for \\(2\\), note that
\\[p\^{2\^n} + 1 \\equiv \\left(\\pm 1\\right)\^{2\^n} + 1 \\equiv 2
\\bmod{4}\\] since our primes are odd. Thus they are all divisible by
\\(2\\) and none by \\(4\\).

Now assume some odd prime \\(p\^{\\ast}\\) divides all of the quantities
in question. We'll show no such \\(p\^{\\ast}\\) can exist by
contradiction.

In much the same way we showed the \\(\\gcd\\) wasn't divisible by
\\(4\\), we seek to find a contradiction in some modulus. But since we
are starting with \\(p\^{2\^n} + 1 \\equiv 0 \\bmod{p\^{\\ast}}\\), if
we can find some such \\(p\\) with \\(p \\equiv 1 \\bmod{p\^{\\ast}}\\),
then we'd have our contradiction from
\\[0 \\equiv p\^{2\^n} + 1 \\equiv 1\^{2\^n} + 1 \\equiv 2
\\bmod{p\^{\\ast}}\\] which can't occur since \\(p\^{\\ast}\\) is an odd
prime.

With this in mind, along with a subsequence of the arithmetic
progression \\(\\left\\{5, 13, 21, 29, \\ldots\\right\\}\\), it seems
that using [Dirichlet's theorem on arithmetic
progressions](http://en.wikipedia.org/wiki/Dirichlet's_theorem_on_arithmetic_progressions) may
be a good strategy. However, this sequence only tells us about the
residue modulo \\(8\\), but we also want to know about the residue
modulo \\(p\^{\\ast}\\). Naturally, we look for a subsequence in
\\[\\mathbb{Z}/\\mathbb{8Z} \\times \\mathbb{Z}/\\mathbb{p\^{\\ast}Z}\\]
corresponding to the residue pair \\((5 \\bmod{8}, 1
\\bmod{p\^{\\ast}})\\). Due to the [Chinese remainder
theorem](http://en.wikipedia.org/wiki/Chinese_remainder_theorem) this
corresponds to a unique residue modulo \\(8p\^{\\ast}\\).

Since this residue \\(r\\) has \\(r \\equiv 1 \\bmod{p\^{\\ast}}\\), we
must have
\\[r \\in \\left\\{1, 1 + p\^{\\ast}, 1 + 2p\^{\\ast}, \\ldots, 1 +
7p\^{\\ast}\\right\\} .\\] But since \\(1 + kp\^{\\ast} \\equiv r
\\equiv 5 \\bmod{8}\\), we have \\(kp\^{\\ast} \\equiv 4 \\bmod{8}\\)
and \\(k \\equiv 4\\left(p\^{\\ast}\\right)\^{-1} \\bmod{8}\\) since
\\(p\^{\\ast}\\) is odd and invertible mod \\(8\\). But this also means
its inverse is odd, hence \\(k \\equiv 4\\cdot(2k' + 1) \\equiv 4
\\bmod{8}\\). Thus we have \\(1 + 4 p\^{\\ast} \\in
\\mathbb{Z}/8p\^{\\ast}\\mathbb{Z}\\) corresponding to our residue
pair. Thus every element in the arithmetic progression \\(S =
\\left\\{(1 + 4p\^{\\ast}) + (8p\^{\\ast})k
\\right\\}\_{k=0}\^{\\infty}\\) is congruent to \\(1 + 4 p\^{\\ast}
\\bmod{8p\^{\\ast}}\\) and hence \\(5 \\bmod{8}\\) and \\(1
\\bmod{p\^{\\ast}}\\).

What's more, since \\(5 \\in
\\left(\\mathbb{Z}/8\\mathbb{Z}\\right)\^{\\times}\\) and \\(1 \\in
\\left(\\mathbb{Z}/p\^{\\ast}\\mathbb{Z}\\right)\^{\\times}\\), we have
\\(1 + 4 p\^{\\ast} \\in
\\left(\\mathbb{Z}/8p\^{\\ast}\\mathbb{Z}\\right)\^{\\times}\\) (again
by the Chinese remainder theorem). Thus the arithmetic progression
\\(S\\) satisfies the hypothesis of Dirichlet's theorem. Hence there
must at least one prime \\(p\\) occurring in the progression (since
there are infinitely many). But that also means \\(p\\) occurs in
\\(\\left\\{5, 13, 29, 37, \\ldots\\right\\}\\) hence we've reached our
desired contradiction. RAA.

<span style="font-size: large;">Now What?</span>
------------------------------------------------

We still don't know if the strong version \\((2)\\)
\\[\\gcd\\left(5\^{2\^n} + 1, 13\^{2\^n} + 1, \\ldots, p\^{2\^n} + 1,
\\ldots \\right) = 2\\] By similar arguments as above, if any odd prime
\\(p\^{\\ast}\\) divides this \\(\\gcd\\), then we have
\\[5\^{2\^n} \\equiv -1 \\bmod{p\^{\\ast}}\\] hence there is an element
of order \\(2\^{n + 1}\\). This means the order of the multiplicative
group \\(\\varphi\\left(p\^{\\ast}\\right) = p\^{\\ast} - 1\\) is
divisible by \\(2\^{n + 1}\\). Beyond that, who knows? We're still
thinking about it (but only passively, more important things to do).

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
