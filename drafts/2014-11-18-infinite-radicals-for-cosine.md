title: TBD
date: 2014-11-18
author: Danny Hermes (dhermes@bossylobster.com)
tags:
slug: infinite-radicals-for-cosine
comments: true

Infinite Radical as Expressions \(2 \cos \pi q\) for \(q\) rational
(NB: UNCLEAR HOW TO PUT KaTeX IN Markdown TITLE)

Note that
\[2 \cos^2 \left(\frac{\theta}{2}\right) - 1 = \cos \theta\]
so that
\[4 \cos^2 \left(\frac{\theta}{2}\right) = 2 + 2 \cos \theta\]
and if we know \(\theta\) enough to say these are all positive, then
\[2 \cos \left(\frac{\theta}{2}\right) = \sqrt{2 + 2 \cos \theta}.\]
For such suitable \(\theta\) we similarly have
\[2 \cos \left(\frac{\pi - \theta}{2}\right) = 2 \sin \left(\frac{\theta}{2}\right) = \sqrt{2 - 2 \cos \theta}.\]
This lets us solve an interesting question of the convergence of the infinite fraction
\[Q(s) = \sqrt{2 + s_1 \sqrt{2 +s_2 \sqrt{2 + s_3 \sqrt{2 + \cdots}}}}\]
given by the sequence of signs
\[s = \left\{s_1, s_2, s_3, \cdots\right\} \subseteq \left\{1, -1\right\}.\]
If we can describe it with a repeating block of signs, e.g.
\[s = \overline{s_1 \ldots s_k},\]
then computation of \(Q(s)\) can be done by setting
\[Q(s) = 2 \cos \left(\pi q(s)\right).\]
For example, if \(s = \overline{+ -}\), then we have
\[Q(s) = \sqrt{2 + \sqrt{2 - Q(s)}}\]
which means
\[2 \cos \left(\pi q(s)\right) = \sqrt{2 + \sqrt{2 - 2 \cos \left(\pi q(s)\right)}}.\]
By the identities above,
\[\sqrt{2 - 2\cos \left(\pi q(s)\right)} = 2 \cos \left(\frac{\pi - \pi q(s)}{2}\right)\]
which means
\[\sqrt{2 + \sqrt{2 - 2 \cos \left(\pi q(s)\right)}} = 2 \cos \left(\frac{\pi - \pi q(s)}{4}\right).\]
Now we can instead solve the much simpler
\[2 \cos \left(\pi q(s)\right) = 2 \cos \left(\frac{\pi - \pi q(s)}{4}\right)\]
or instead just solve
\[q = \frac{1 - q}{4}.\]
This gives \(q\left(\overline{+-}\right) = \frac{1}{5}\) and \(Q\left(\overline{+-}\right) = 2 \cos \left(\pi q\left(\overline{+-}\right)\right) = 2 \cos \left(\frac{\pi}{5}\right)\).
