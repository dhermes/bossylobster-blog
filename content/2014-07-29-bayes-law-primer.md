Title: Bayes' Law Primer
date: 2014-07-29
author: Danny Hermes (dhermes@bossylobster.com)
tags: Bayes, Layman, Mathematics, Probability
slug: bayes-law-primer

I'm currently writing a blog post that uses [Bayes'
Law](http://en.wikipedia.org/wiki/Bayes%27_law) but don't want to muddy
the post with a review in layman's terms. So I have something to link,
here is a short description and a chance to flex my
[teaching](http://math.berkeley.edu/~dhermes/) muscles before the school
year starts.

Bayes' Law
----------

For those who aren't sure, Bayes' Law tells us that the probability
event \\(X\\) occurs given we know that event \\(Y\\) has occurred can
easily be computed. It is written as \\(\\text{Pr}(X \\mid Y)\\) and the
vertical bar is meant like the word "given", in other words, the event
\\(X\\) is distinct from the event \\(X \\mid Y\\) (\\(X\\) given
\\(Y\\)). Bayes' law, states that
\\[\\text{Pr}(X \\mid Y) = \\frac{\\text{Pr}(X \\text{ and } Y \\text{
both occur})}{\\text{Pr}(Y)}.\\]
This effectively is a re-scaling of the events by the total probability
of the given event: \\(\\text{Pr}(Y)\\).

For example, if \\(X\\) is the event that a \\(3\\) is rolled on a fair
die and \\(Y\\) is the event that the roll is odd. We know of course
that \\(\\text{Pr}(Y) = \\frac{1}{2}\\) since half of the rolls are odd.
The event \\(X \\text{ and } Y \\text{ both occur}\\) in this case is
the same as \\(X\\) since the roll can only be \\(3\\) is the roll is
odd. Thus
\\[\\text{Pr}(X \\text{ and } Y \\text{ both occur}) = \\frac{1}{6}\\]
and we can compute the conditional probability
\\[\\text{Pr}(X \\mid Y) = \\frac{\\frac{1}{6}}{\\frac{1}{2}} =
\\frac{1}{3}.\\]
As we expect, one out of every three odd rolls is a \\(3\\).

Bayes' Law Extended Form {#extended}
------------------------

Instead of considering a single event \\(Y\\), we can consider a range
of \\(n\\) possible events \\(Y\_1, Y\_2, \\ldots, Y\_n\\) that may
occur. We require that one of these \\(Y\\)-events must occur and that
they cover all possible events that could occur. For example \\(Y\_1\\)
is the event that H2O is vapor, \\(Y\_2\\) is the event that H2O is
water and\\(Y\_3\\) is the event that H2O is ice.

In such a case we know that since the \\(Y\\)-events are distinct
\\[\\text{Pr}(X) = \\text{Pr}(X \\text{ and } Y\_1 \\text{ both occur})
+ \\text{Pr}(X \\text{ and } Y\_2 \\text{ both occur}) + \\text{Pr}(X
\\text{ and } Y\_3 \\text{ both occur}).\\]
Using Bayes' law, we can reinterpret as
\\[\\text{Pr}(X \\text{ and } Y\_j \\text{ both occur}) =  \\text{Pr}(X
\\mid Y\_j) \\cdot \\text{Pr}(Y\_j)\\]
and the above becomes
\\[\\text{Pr}(X) = \\text{Pr}(X \\mid Y\_1) \\cdot \\text{Pr}(Y\_1)
+ \\text{Pr}(X \\mid Y\_2) \\cdot \\text{Pr}(Y\_2) + \\text{Pr}(X \\mid
Y\_3) \\cdot \\text{Pr}(Y\_3).\\]
The same is true if we replace \\(3\\) with an arbitrary number of
events \\(n\\).

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
