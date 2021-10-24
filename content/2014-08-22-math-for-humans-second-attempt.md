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
<html-literal>3c7370616e20636c6173733d226b617465782d646973706c6179223e3c7370616e20636c6173733d226b61746578223e3c7370616e20636c6173733d226b617465782d6d6174686d6c223e3c6d61746820786d6c6e733d22687474703a2f2f7777772e77332e6f72672f313939382f4d6174682f4d6174684d4c2220646973706c61793d22626c6f636b223e3c73656d616e746963733e3c6d726f773e3c6d667261633e3c6d6e3e31323c2f6d6e3e3c6d6e3e32393c2f6d6e3e3c2f6d667261633e3c6d6f3e2623383737363b3c2f6d6f3e3c6d6e3e302e3431333739333130333c2f6d6e3e3c2f6d726f773e3c616e6e6f746174696f6e20656e636f64696e673d226170706c69636174696f6e2f782d746578223e5c667261637b31327d7b32397d205c617070726f7820302e3431333739333130333c2f616e6e6f746174696f6e3e3c2f73656d616e746963733e3c2f6d6174683e3c2f7370616e3e3c7370616e20636c6173733d226b617465782d68746d6c2220617269612d68696464656e3d2274727565223e3c7370616e20636c6173733d2262617365223e3c7370616e20636c6173733d22737472757422207374796c653d226865696768743a322e3030373434656d3b766572746963616c2d616c69676e3a2d302e363836656d3b223e3c2f7370616e3e3c7370616e20636c6173733d226d6f7264223e3c7370616e20636c6173733d226d6f70656e206e756c6c64656c696d69746572223e3c2f7370616e3e3c7370616e20636c6173733d226d66726163223e3c7370616e20636c6173733d22766c6973742d7420766c6973742d7432223e3c7370616e20636c6173733d22766c6973742d72223e3c7370616e20636c6173733d22766c69737422207374796c653d226865696768743a312e3332313434656d3b223e3c7370616e207374796c653d22746f703a2d322e333134656d3b223e3c7370616e20636c6173733d2270737472757422207374796c653d226865696768743a33656d3b223e3c2f7370616e3e3c7370616e20636c6173733d226d6f7264223e3c7370616e20636c6173733d226d6f7264223e32393c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c7370616e207374796c653d22746f703a2d332e3233656d3b223e3c7370616e20636c6173733d2270737472757422207374796c653d226865696768743a33656d3b223e3c2f7370616e3e3c7370616e20636c6173733d22667261632d6c696e6522207374796c653d22626f726465722d626f74746f6d2d77696474683a302e3034656d3b223e3c2f7370616e3e3c2f7370616e3e3c7370616e207374796c653d22746f703a2d332e363737656d3b223e3c7370616e20636c6173733d2270737472757422207374796c653d226865696768743a33656d3b223e3c2f7370616e3e3c7370616e20636c6173733d226d6f7264223e3c7370616e20636c6173733d226d6f7264223e31323c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c7370616e20636c6173733d22766c6973742d73223e2623383230333b3c2f7370616e3e3c2f7370616e3e3c7370616e20636c6173733d22766c6973742d72223e3c7370616e20636c6173733d22766c69737422207374796c653d226865696768743a302e363836656d3b223e3c7370616e3e3c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c7370616e20636c6173733d226d636c6f7365206e756c6c64656c696d69746572223e3c2f7370616e3e3c2f7370616e3e3c7370616e20636c6173733d226d737061636522207374796c653d226d617267696e2d72696768743a302e32373737373737373737373737373738656d3b223e3c2f7370616e3e3c7370616e20636c6173733d226d72656c223e2623383737363b3c2f7370616e3e3c7370616e20636c6173733d226d737061636522207374796c653d226d617267696e2d72696768743a302e32373737373737373737373737373738656d3b223e3c2f7370616e3e3c2f7370616e3e3c7370616e20636c6173733d2262617365223e3c7370616e20636c6173733d22737472757422207374796c653d226865696768743a302e3634343434656d3b766572746963616c2d616c69676e3a30656d3b223e3c2f7370616e3e3c7370616e20636c6173733d226d6f7264223e302e3431333739333130333c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c2f7370616e3e3c2f7370616e3e</html-literal>
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
