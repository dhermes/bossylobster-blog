title: Conditional Probabilities in "Thinking Fast and Slow"
date: 2014-07-29
author: Danny Hermes (dhermes@bossylobster.com)
tags: Bayes, Bayesian, Kahneman, Layman, Mathematics, Probability
slug: conditional-probabilities-in-thinking
comments: true

I'm currently reading
<a href="http://www.amazon.com/gp/product/0374533555/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0374533555&linkCode=as2&tag=boslobblo-20&linkId=FMJCYK4RKIVWRNFH">Thinking, Fast and Slow</a><img src="//ir-na.amazon-adsystem.com/e/ir?t=boslobblo-20&l=as2&o=1&a=0374533555" width="1" height="1" border="0" alt="AMZN Affiliate Ad" style="border:none !important; margin:0px !important;" />
by [Daniel Kahneman](http://en.wikipedia.org/wiki/Daniel_Kahneman).
(Thanks to Elianna for letting me borrow it.) I'm not finished yet, but
60% of the way through I definitely recommend it.

While reading the "Causes Trump Statistics" chapter (number 16), there
is a description of a study about cabs and hit-and-run accidents. It
describes a scenario where participants are told that 85% of cabs are
Green, 15% are Blue and a given observer has an 80% chance of correctly
identifying the color of a given cab. Given this data, the chapter
presents a scenario where a bystander identifies a cab in an accident as
Blue and Kahneman goes on to explain how we fail to take the data into
consideration. I really enjoyed this chapter, but won't wreck the book
for you.

Instead, I want to do some math (big surprise, I know). However, I want
to make it accessible to non-mathematicians (atypical for my posts).

Given the data, Kahneman tells us that the true probability that the cab
was Blue is 41% though we likely bias our thinking towards the 80%
probability of the identification being correct. I was on the
[bus](http://www.sfmta.com/) and it kept bothering me, to the point that
I couldn't continue reading. Eventually I figured it out (when I got to
the [train](http://www.bart.gov/)) and I wanted to explain how this is
computed using [Bayes' Law](http://en.wikipedia.org/wiki/Bayes%27_law).
As a primer, I wrote a
[post](/2014/07/bayes-law-primer.html) using
layman's terms explaining how we use Bayes' Law. (There is some notation
introduced but I hope it isn't too confusing.)

Putting Bayes' Law to Use
-------------------------

We need to understand what 41% even corresponds to before we can compute
it. What's actually happened is that we know the event
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>I</mi><mi>D</mi><mi>B</mi></mrow><annotation encoding="application/x-tex">IDB</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.68333em;vertical-align:0em;"></span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span></span></span></span> has occurred -- the cab has been identified
(<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>I</mi><mi>D</mi></mrow><annotation encoding="application/x-tex">ID</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.68333em;vertical-align:0em;"></span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span></span></span></span>) as Blue (<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>B</mi></mrow><annotation encoding="application/x-tex">B</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.68333em;vertical-align:0em;"></span><span class="mord mathit" style="margin-right:0.05017em;">B</span></span></span></span>).
What we want is the probability that the cab **is Blue** given we know
it has been identified -- we want:

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo><mi mathvariant="normal">.</mi></mrow><annotation encoding="application/x-tex">\text{Pr}(B \, | \, IDB).</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mord">.</span></span></span></span>
</blockquote></div>

Using Bayes' Law, we can write

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo><mo>=</mo><mfrac><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mtext>&#0160;and&#0160;</mtext><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&#0160;both&#0160;occur</mtext><mo>)</mo></mrow><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo></mrow></mfrac></mrow><annotation encoding="application/x-tex">\text{Pr}(B \, | \, IDB) = \frac{\text{Pr}(B \text{ and } IDB \text{ both occur})}{\text{Pr}(IDB)}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:1.53em;vertical-align:-0.52em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:1.01em;"><span style="top:-2.655em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord text mtight"><span class="mord mtight">Pr</span></span><span class="mopen mtight">(</span><span class="mord mathit mtight" style="margin-right:0.07847em;">I</span><span class="mord mathit mtight" style="margin-right:0.02778em;">D</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mclose mtight">)</span></span></span></span><span style="top:-3.23em;"><span class="pstrut" style="height:3em;"></span><span class="frac-line" style="border-bottom-width:0.04em;"></span></span><span style="top:-3.485em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord text mtight"><span class="mord mtight">Pr</span></span><span class="mopen mtight">(</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mord text mtight"><span class="mord mtight">&#0160;and&#0160;</span></span><span class="mord mathit mtight" style="margin-right:0.07847em;">I</span><span class="mord mathit mtight" style="margin-right:0.02778em;">D</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mord text mtight"><span class="mord mtight">&#0160;both&#0160;occur</span></span><span class="mclose mtight">)</span></span></span></span></span><span class="vlist-s">&#8203;</span></span><span class="vlist-r"><span class="vlist" style="height:0.52em;"><span></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span>
</blockquote></div>

and

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>B</mi><mo>)</mo><mo>=</mo><mfrac><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mtext>&#0160;and&#0160;</mtext><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&#0160;both&#0160;occur</mtext><mo>)</mo></mrow><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mo>)</mo></mrow></mfrac><mi mathvariant="normal">.</mi></mrow><annotation encoding="application/x-tex">\text{Pr}(IDB \, | \, B) = \frac{\text{Pr}(B \text{ and } IDB \text{ both occur})}{\text{Pr}(B)}.</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:1.53em;vertical-align:-0.52em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:1.01em;"><span style="top:-2.655em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord text mtight"><span class="mord mtight">Pr</span></span><span class="mopen mtight">(</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mclose mtight">)</span></span></span></span><span style="top:-3.23em;"><span class="pstrut" style="height:3em;"></span><span class="frac-line" style="border-bottom-width:0.04em;"></span></span><span style="top:-3.485em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord text mtight"><span class="mord mtight">Pr</span></span><span class="mopen mtight">(</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mord text mtight"><span class="mord mtight">&#0160;and&#0160;</span></span><span class="mord mathit mtight" style="margin-right:0.07847em;">I</span><span class="mord mathit mtight" style="margin-right:0.02778em;">D</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mord text mtight"><span class="mord mtight">&#0160;both&#0160;occur</span></span><span class="mclose mtight">)</span></span></span></span></span><span class="vlist-s">&#8203;</span></span><span class="vlist-r"><span class="vlist" style="height:0.52em;"><span></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mord">.</span></span></span></span>
</blockquote></div>

identified 80% of the time hence

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>B</mi><mo>)</mo><mo>=</mo><mn>0.8</mn></mrow><annotation encoding="application/x-tex">\text{Pr}(IDB \, | \, B) = 0.8</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">8</span></span></span></span>
</blockquote></div>

(i.e. the probability of correct ID
as Blue given it is actually Blue). We're also told that 15% of the cabs
are Blue hence

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mo>)</mo><mo>=</mo><mn>0.15.</mn></mrow><annotation encoding="application/x-tex">\text{Pr}(B) = 0.15.</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">1</span><span class="mord">5</span><span class="mord">.</span></span></span></span>
</blockquote></div>

 We can combine these with the second
application of Bayes' Law above to show that

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mtext>&#0160;and&#0160;</mtext><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&#0160;both&#0160;occur</mtext><mo>)</mo><mo>=</mo><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>B</mi><mo>)</mo><mo>&#8901;</mo><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mo>)</mo><mo>=</mo><mn>0.12.</mn></mrow><annotation encoding="application/x-tex">\text{Pr}(B \text{ and } IDB \text{ both occur}) = \text{Pr}(IDB \, | \, B) \cdot \text{Pr}(B) = 0.12.</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mord text"><span class="mord">&#0160;and&#0160;</span></span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mord text"><span class="mord">&#0160;both&#0160;occur</span></span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">&#8901;</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">1</span><span class="mord">2</span><span class="mord">.</span></span></span></span>
</blockquote></div>

The only piece of data missing now to finish our computation is
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">\text{Pr}(IDB)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span></span></span></span>.

Using the
[extended form](ster.com/2014/07/bayes-law-primer.html#extended)
of Bayes' Law, since we know that the events <span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>B</mi></mrow><annotation encoding="application/x-tex">B</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.68333em;vertical-align:0em;"></span><span class="mord mathit" style="margin-right:0.05017em;">B</span></span></span></span> and
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>G</mi></mrow><annotation encoding="application/x-tex">G</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.68333em;vertical-align:0em;"></span><span class="mord mathit">G</span></span></span></span> (the cab is Blue or Green) are exclusive and cover all
possibilities for the cab, we can say that

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo><mo>=</mo><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>B</mi><mo>)</mo><mo>&#8901;</mo><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mo>)</mo><mo>+</mo><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>G</mi><mo>)</mo><mo>&#8901;</mo><mtext>Pr</mtext><mo>(</mo><mi>G</mi><mo>)</mo><mi mathvariant="normal">.</mi></mrow><annotation encoding="application/x-tex">\text{Pr}(IDB) = \text{Pr}(IDB \, | \, B) \cdot \text{Pr}(B) + \text{Pr}(IDB \, | \, G) \cdot \text{Pr}(G).</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">&#8901;</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit">G</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">&#8901;</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit">G</span><span class="mclose">)</span><span class="mord">.</span></span></span></span>
</blockquote></div>

Since there is only an 80% chance of correct identification, we know that
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>G</mi><mo>)</mo><mo>=</mo><mn>0.2</mn></mrow><annotation encoding="application/x-tex">\text{Pr}(IDB \, | \, G) = 0.2</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit">G</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">2</span></span></span></span> (the probability of
misidentifying a Green cab as Blue). We also know that 85% of the cabs are
Green hence we can plug these in (along with numbers already computed) to get

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo><mo>=</mo><mn>0.8</mn><mo>&#8901;</mo><mn>0.15</mn><mo>+</mo><mn>0.2</mn><mo>&#8901;</mo><mn>0.85</mn><mo>=</mo><mn>0.12</mn><mo>+</mo><mn>0.17</mn><mo>=</mo><mn>0.29.</mn></mrow><annotation encoding="application/x-tex">\text{Pr}(IDB) = 0.8 \cdot 0.15 + 0.2 \cdot 0.85 = 0.12 + 0.17 = 0.29.</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">8</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">&#8901;</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:0.72777em;vertical-align:-0.08333em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">1</span><span class="mord">5</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">2</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">&#8901;</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">8</span><span class="mord">5</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.72777em;vertical-align:-0.08333em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">1</span><span class="mord">2</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222222222222222em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">1</span><span class="mord">7</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">2</span><span class="mord">9</span><span class="mord">.</span></span></span></span>
</blockquote></div>

Putting it all together we get our answer

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mtext>&ThinSpace;</mtext><mi mathvariant="normal">&#8739;</mi><mtext>&ThinSpace;</mtext><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo><mo>=</mo><mfrac><mrow><mtext>Pr</mtext><mo>(</mo><mi>B</mi><mtext>&#0160;and&#0160;</mtext><mi>I</mi><mi>D</mi><mi>B</mi><mtext>&#0160;both&#0160;occur</mtext><mo>)</mo></mrow><mrow><mtext>Pr</mtext><mo>(</mo><mi>I</mi><mi>D</mi><mi>B</mi><mo>)</mo></mrow></mfrac><mo>=</mo><mfrac><mn>0.12</mn><mn>0.29</mn></mfrac><mo>&#8776;</mo><mn>0.413793103.</mn></mrow><annotation encoding="application/x-tex">\text{Pr}(B \, | \, IDB) = \frac{\text{Pr}(B \text{ and } IDB \text{ both occur})}{\text{Pr}(IDB)} = \frac{0.12}{0.29} \approx 0.413793103.</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">Pr</span></span><span class="mopen">(</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord">&#8739;</span><span class="mspace" style="margin-right:0.16666666666666666em;"></span><span class="mord mathit" style="margin-right:0.07847em;">I</span><span class="mord mathit" style="margin-right:0.02778em;">D</span><span class="mord mathit" style="margin-right:0.05017em;">B</span><span class="mclose">)</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:1.53em;vertical-align:-0.52em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:1.01em;"><span style="top:-2.655em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord text mtight"><span class="mord mtight">Pr</span></span><span class="mopen mtight">(</span><span class="mord mathit mtight" style="margin-right:0.07847em;">I</span><span class="mord mathit mtight" style="margin-right:0.02778em;">D</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mclose mtight">)</span></span></span></span><span style="top:-3.23em;"><span class="pstrut" style="height:3em;"></span><span class="frac-line" style="border-bottom-width:0.04em;"></span></span><span style="top:-3.485em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord text mtight"><span class="mord mtight">Pr</span></span><span class="mopen mtight">(</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mord text mtight"><span class="mord mtight">&#0160;and&#0160;</span></span><span class="mord mathit mtight" style="margin-right:0.07847em;">I</span><span class="mord mathit mtight" style="margin-right:0.02778em;">D</span><span class="mord mathit mtight" style="margin-right:0.05017em;">B</span><span class="mord text mtight"><span class="mord mtight">&#0160;both&#0160;occur</span></span><span class="mclose mtight">)</span></span></span></span></span><span class="vlist-s">&#8203;</span></span><span class="vlist-r"><span class="vlist" style="height:0.52em;"><span></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:1.190108em;vertical-align:-0.345em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.845108em;"><span style="top:-2.6550000000000002em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">0</span><span class="mord mtight">.</span><span class="mord mtight">2</span><span class="mord mtight">9</span></span></span></span><span style="top:-3.23em;"><span class="pstrut" style="height:3em;"></span><span class="frac-line" style="border-bottom-width:0.04em;"></span></span><span style="top:-3.394em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">0</span><span class="mord mtight">.</span><span class="mord mtight">1</span><span class="mord mtight">2</span></span></span></span></span><span class="vlist-s">&#8203;</span></span><span class="vlist-r"><span class="vlist" style="height:0.345em;"><span></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">&#8776;</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">4</span><span class="mord">1</span><span class="mord">3</span><span class="mord">7</span><span class="mord">9</span><span class="mord">3</span><span class="mord">1</span><span class="mord">0</span><span class="mord">3</span><span class="mord">.</span></span></span></span>
</blockquote></div>

Fantastic! Now we can get back to reading...