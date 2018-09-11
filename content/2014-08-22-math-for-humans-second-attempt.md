---
title: Math for Humans, A Second Attempt
date: 2014-08-22
author: Danny Hermes (dhermes@bossylobster.com)
tags: Bayes, Bayesian, Kahneman, Layman, Mathematics, Probability
slug: math-for-humans-second-attempt
comments: true
github_slug: templated_content/2014-08-22-math-for-humans-second-attempt.template
---

The morning after posting my latest
[blog post](/2014/07/conditional-probabilities-in-thinking.html),
I woke up still thinking about how to explain the concept.

More importantly, I realized that my goal of writing
**math for humans** failed miserably.

So here is a second go at it.

First we're told we're in a world where **85% of cabs are Green**
and the rest are Blue. Humans love tables (and they are
easy to understand). So we start off with a representative sample of 100
cabs:

<!--- http://blogknowhow.blogspot.com/2011/01/how-add-table-blogger-blogspot-post.html -->
<style type="text/css">
.nobrtable br { display: none }
.nobrtable tr {text-align: center;}
.nobrtable tr.alt td {background-color: #eeeecc; color: black;}
.nobrtable td {text-align: center;}
.nobrtable caption {caption-side:bottom;}
</style>

<div style="margin-left: auto; margin-right: auto; text-align: center;">
<div class="nobrtable">
<table border="2" bordercolor="#0033FF" cellpadding="10" cellspacing="0" style="background-color: #99ffff; border-collapse: collapse; color: black; margin-left: auto; margin-right: auto; width: 100%px;">
<tbody>
<tr style="background-color: #0033ff; color: white; padding-bottom: 4px; padding-top: 5px;">
<th>Category</th>
<th>Green</th>
<th>Blue</th>
<th>Total</th>
</tr>
<tr class="alt">
<td>Cabs</td>
<td>85</td>
<td>15</td>
<td>100</td>
</tr>
</tbody></table>
</div>
</div>

After this, we're told that a bystander
**correctly identifies a cab 80% of the time**, or 4 out of every 5.
Applying this to the 85 Green cabs (85 is 17 times 5), this bystander
will mis-identify 17 as Blue (1 out of 5) and the other 68 will
correctly be identified as Green:

<div style="margin-left: auto; margin-right: auto; text-align: center;">
<div class="nobrtable">
<table border="2" bordercolor="#0033FF" cellpadding="10" cellspacing="0" style="background-color: #99ffff; border-collapse: collapse; color: black; margin-left: auto; margin-right: auto; width: 100%px;">
<tbody>
<tr style="background-color: #0033ff; color: white; padding-bottom: 4px; padding-top: 5px;">
<th>Category</th>
<th>Green</th>
<th>Blue</th>
<th>Total</th>
</tr>
<tr class="alt">
<td>Cabs</td>
<td>85</td>
<td>15</td>
<td>100</td>
</tr>
<tr>
<td>ID'd Green</td>
<td><b>68</b></td>
<td></td>
<td></td>
</tr>
<tr class="alt">
<td>ID'd Blue</td>
<td><b>17</b></td>
<td></td>
<td></td>
</tr>
</tbody></table>
</div>
</div>

Similarly, of the 15 Blue cabs (15 is 3 times 5), this bystander will
mis-identify 3 as Green (1 out of 5) and the other 12 will correctly be
identified as Blue:

<div style="margin-left: auto; margin-right: auto; text-align: center;">
<div class="nobrtable">
<table border="2" bordercolor="#0033FF" cellpadding="10" cellspacing="0" style="background-color: #99ffff; border-collapse: collapse; color: black; margin-left: auto; margin-right: auto; width: 100%px;">
<tbody>
<tr style="background-color: #0033ff; color: white; padding-bottom: 4px; padding-top: 5px;">
<th>Category</th>
<th>Green</th>
<th>Blue</th>
<th>Total</th>
</tr>
<tr class="alt">
<td>Cabs</td>
<td>85</td>
<td>15</td>
<td>100</td>
</tr>
<tr>
<td>ID'd Green</td>
<td>68</td>
<td><b>3</b></td>
<td></td>
</tr>
<tr class="alt">
<td>ID'd Blue</td>
<td>17</td>
<td><b>12</b></td>
<td></td>
</tr>
</tbody></table>
</div>
</div>

Now Kahneman wants us to use the data at hand to determine what the
probability is that a cab is <span>actually Blue</span> given the
bystander **identified the cab as Blue**. To determine this
probability, we simply need to consider the final row of the table:

<div style="margin-left: auto; margin-right: auto; text-align: center;">
<div class="nobrtable">
<table border="2" bordercolor="#0033FF" cellpadding="10" cellspacing="0" style="background-color: #99ffff; border-collapse: collapse; color: black; margin-left: auto; margin-right: auto; width: 100%px;">
<tbody>
<tr style="background-color: #0033ff; color: white; padding-bottom: 4px; padding-top: 5px;">
<th>Category</th>
<th>Green</th>
<th>Blue</th>
<th>Total</th>
</tr>
<tr class="alt">
<td>ID'd Blue</td>
<td>17</td>
<td>12</td>
<td><b>29</b></td>
</tr>
</tbody></table>
</div>
</div>

This rows tells us that only 29 cabs will be identified as Blue, and
among those, 12 will actually be Blue. Hence the probability will be

<div class="katex-elt"><blockquote>
<span class="katex"><span class="katex-mathml"><math><semantics><mrow><mfrac><mn>12</mn><mn>29</mn></mfrac><mo>&#8776;</mo><mn>0.413793103</mn></mrow><annotation encoding="application/x-tex">\frac{12}{29} \approx 0.413793103</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1.190108em;vertical-align:-0.345em;"></span><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.845108em;"><span style="top:-2.6550000000000002em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">2</span><span class="mord mtight">9</span></span></span></span><span style="top:-3.23em;"><span class="pstrut" style="height:3em;"></span><span class="frac-line" style="border-bottom-width:0.04em;"></span></span><span style="top:-3.394em;"><span class="pstrut" style="height:3em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">1</span><span class="mord mtight">2</span></span></span></span></span><span class="vlist-s">&#8203;</span></span><span class="vlist-r"><span class="vlist" style="height:0.345em;"><span></span></span></span></span></span><span class="mclose nulldelimiter"></span></span><span class="mspace" style="margin-right:0.2777777777777778em;"></span><span class="mrel">&#8776;</span><span class="mspace" style="margin-right:0.2777777777777778em;"></span></span><span class="base"><span class="strut" style="height:0.64444em;vertical-align:0em;"></span><span class="mord">0</span><span class="mord">.</span><span class="mord">4</span><span class="mord">1</span><span class="mord">3</span><span class="mord">7</span><span class="mord">9</span><span class="mord">3</span><span class="mord">1</span><span class="mord">0</span><span class="mord">3</span></span></span></span>
</blockquote></div>

What this really shows is that even though the bystander has a large
chance (80%) of getting the color right, the number of Green cabs is
so much larger it overwhelms the correctly identified Blue cabs with
incorrectly identified Green ones.

What I Overlooked
-----------------

-   Dense text is always bad
-   Using colors and breaking up text makes reading easier (more
    modular)
-   Introducing mathematical notation is almost always overkill
-   Tables and samples are a good way to discuss probabilities
