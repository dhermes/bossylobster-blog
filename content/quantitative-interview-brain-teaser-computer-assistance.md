Title: Quantitative Interview Brain Teaser: Computer Assistance
Date: 2014-09-29 01:25
Author: Danny Hermes (noreply@blogger.com)
Tags: Brain Teaser, Combinatorics, Digit Counting, Interview Questions, itertools, Mathematics, Programming, Python
Slug: quantitative-interview-brain-teaser-computer-assistance

<p>
In a [previous
post](http://blog.bossylobster.com/2014/09/quantitative-brain-teaser-brain-only.html)
I discussed a recent brain teaser I had come across:   

> Find a <span>10-digit number</span>, where each digit represents the
> number of that ordinal number in the whole number. So, the <span>first
> digit represents the number of 0's</span> in the whole 10 digits. The
> second digit represents the number of 1's in the whole 10 digits. And
> so on. The first digit is not a 0.

As I promised at the end of the "brain only" post, we'll do better than
simply finding **an** answer, we'll find all of them (with the aid of a
computer).

* * * * *

#### Making the Problem Smaller

Without any thinking, there are 9 billion (<span class="katex"><span
class="katex-inner"><span class="strut"
style="height: 0.8141079999999999em;"></span><span class="strut bottom"
style="height: 0.8141079999999999em; vertical-align: 0em;"></span><span
class="base textstyle uncramped"><span class="mord">9</span><span
class="mbin">⋅</span><span class="mord">1</span><span class="mord"><span
class="mord">0</span><span class="vlist"><span><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle uncramped"><span
class="mord">9</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span></span></span></span>)
total choices. This is not only intractable for the human brain, but
becomes difficult for a computer too. A 3 GHz processor in the most
optimal case can only perform 3 billion operations per second but there
is a lot of counting, lists to create, and otherwise to find a number
which fits the criteria. To start, we write our number as

<div style="text-align: center;">

> <span style="font-size: x-large;"><span class="katex"><span
> class="katex-inner"><span class="strut"
> style="height: 0.69444em;"></span><span
> class="strut bottom"></span><span
> class="base textstyle uncramped"><span
> class="reset-textstyle displaystyle textstyle uncramped"><span
> class="mord mathit">n</span><span class="mrel">=</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">0</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mpunct">,</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">1</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">2</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">3</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mpunct">,</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">4</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">5</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">6</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mpunct">,</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">7</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">8</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">9</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mord">.</span></span></span></span></span></span>

</div>

Since there are 10 digits in total and each of the digits represent a
subcount of occurrences, the total number of occurrences can be
represented as the sum:

<div style="text-align: center;">

> <span style="font-size: x-large;"><span class="katex"><span
> class="katex-inner"><span class="strut"
> style="height: 0.69444em;"></span><span
> class="strut bottom"></span><span
> class="base textstyle uncramped"><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">0</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">1</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">2</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">3</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">4</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">5</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">6</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">7</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">8</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">9</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mrel">=</span><span class="mord">1</span><span
> class="mord">0</span></span></span></span></span>

</div>

Additionally, (for example) since each 3 contributes a value of 3 to the
digit sum, we must also have

<div style="text-align: center;">

> <span style="font-size: 22px;"><span class="katex"><span
> class="katex-inner"><span class="strut"
> style="height: 0.69444em;"></span><span
> class="strut bottom"></span><span
> class="base textstyle uncramped"><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">1</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">2</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">2</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">3</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">3</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">4</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">4</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">5</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">5</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">6</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">6</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">7</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">7</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">8</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">8</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mbin">+</span><span class="mord">9</span><span
> class="mord"><span class="mord mathit">d</span><span
> class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">9</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mrel">=</span><span class="mord">1</span><span
> class="mord">0</span></span></span></span></span>

</div>

This second equation (which requires the first to make sense) limits our
choices of digits a great deal:

<div style="text-align: center;">

> <span style="font-size: x-large;"><span class="katex"><span
> class="katex-inner"><span class="strut"
> style="height: 0.69444em;"></span><span
> class="strut bottom"></span><span
> class="base textstyle uncramped"><span class="mord">0</span><span
> class="mrel">≤</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">5</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mpunct">,</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">6</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mpunct">,</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">7</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mpunct">,</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">8</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mpunct">,</span><span class="mord"><span
> class="mord mathit">d</span><span class="vlist"><span
> style="margin-right: 0.05em; margin-left: 0em;"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span><span
> class="reset-textstyle scriptstyle cramped"><span
> class="mord">9</span></span></span><span class="baseline-fix"><span
> class="fontsize-ensurer reset-size5 size5"><span
> style="font-size: 0em;">​</span></span>​</span></span></span><span
> class="mrel">≤</span><span
> class="mord">1</span></span></span></span></span>

</div>

The last four are obvious since (for example) <span class="katex"><span
class="katex-inner"><span class="strut"
style="height: 0.64444em;"></span><span
class="strut bottom"></span><span class="base textstyle uncramped"><span
class="mord">2</span><span class="mbin">⋅</span><span
class="mord">6</span><span class="mrel">\></span><span
class="mord">1</span><span class="mord">0</span></span></span></span>.
We can also say that <span class="katex"><span class="katex-inner"><span
class="strut" style="height: 0.69444em;"></span><span
class="strut bottom"></span><span class="base textstyle uncramped"><span
class="mord"><span class="mord mathit">d</span><span class="vlist"><span
style="margin-right: 0.05em; margin-left: 0em;"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle cramped"><span
class="mord">5</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span><span
class="mrel">\<</span><span class="mord">2</span></span></span></span>.
It is clearly no bigger than 2 but in the case that <span
class="katex"><span class="katex-inner"><span class="strut"
style="height: 0.69444em;"></span><span
class="strut bottom"></span><span class="base textstyle uncramped"><span
class="mord"><span class="mord mathit">d</span><span class="vlist"><span
style="margin-right: 0.05em; margin-left: 0em;"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle cramped"><span
class="mord">5</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span><span
class="mrel">=</span><span class="mord">2</span></span></span></span>
we'd also have <span class="katex"><span class="katex-inner"><span
class="strut" style="height: 0.69444em;"></span><span
class="strut bottom"></span><span class="base textstyle uncramped"><span
class="mord"><span class="mord mathit">d</span><span class="vlist"><span
style="margin-right: 0.05em; margin-left: 0em;"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle cramped"><span
class="mord">2</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span><span
class="mrel">\></span><span class="mord">0</span></span></span></span>
meaning <span class="katex"><span class="katex-inner"><span
class="strut" style="height: 0.69444em;"></span><span
class="strut bottom"></span><span class="base textstyle uncramped"><span
class="mord">2</span><span class="mord"><span
class="mord mathit">d</span><span class="vlist"><span
style="margin-right: 0.05em; margin-left: 0em;"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle cramped"><span
class="mord">2</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span><span
class="mbin">+</span><span class="mord">5</span><span class="mord"><span
class="mord mathit">d</span><span class="vlist"><span
style="margin-right: 0.05em; margin-left: 0em;"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle cramped"><span
class="mord">5</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span><span
class="mrel">=</span><span class="mord">2</span><span class="mord"><span
class="mord mathit">d</span><span class="vlist"><span
style="margin-right: 0.05em; margin-left: 0em;"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle cramped"><span
class="mord">2</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span><span
class="mbin">+</span><span class="mord">1</span><span
class="mord">0</span><span class="mrel">\></span><span
class="mord">1</span><span class="mord">0</span></span></span></span>.
Thus to brute force the problem we can choose digits 5 through 9 (5
digits in total) from the 32 (<span class="katex"><span
class="katex-inner"><span class="strut"
style="height: 0.8141079999999999em;"></span><span class="strut bottom"
style="height: 0.8141079999999999em; vertical-align: 0em;"></span><span
class="base textstyle uncramped"><span class="mord"><span
class="mord">2</span><span class="vlist"><span><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle uncramped"><span
class="mord">5</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span></span></span></span>)
different possible ways to make them 0 or 1.

* * * * *

#### Listing All Choices

Now for the fun part: programming (in Python). We now have 90,000 (<span
class="katex"><span class="katex-inner"><span class="strut"
style="height: 0.8141079999999999em;"></span><span class="strut bottom"
style="height: 0.8141079999999999em; vertical-align: 0em;"></span><span
class="base textstyle uncramped"><span class="mord">9</span><span
class="mbin">⋅</span><span class="mord">1</span><span class="mord"><span
class="mord">0</span><span class="vlist"><span><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span><span
class="reset-textstyle scriptstyle uncramped"><span
class="mord">4</span></span></span><span class="baseline-fix"><span
class="fontsize-ensurer reset-size5 size5"><span
style="font-size: 0em;">​</span></span>​</span></span></span></span></span></span>)
choices for our first 5 digits and 32 choices for our last 5 digits. We
can use Python's <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">range(10\*\*4,
10\*\*5)</span> to represent the 5-digit numbers between 10,000 and
99,999 (inclusive). For the 32 choices for the last 5 digits, we use
<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">itertools.product</span>.
To see it in action on a smaller set of data: When we ask for 5 repeated
copies of the tuple <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">(0,
1)</span> we get 32 possible 5-tuples as expected:

* * * * *

#### Checking Candidates

Before we can iterate through all of our combinations, we need a way to
check if a given number fits the criterion. To do that we implement This
takes a <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">list</span>
of digits, so as we loop over all choices, we'll turn them into lists.

* * * * *

#### Exhaustive Search

Now we can use our accumulated tools, loop through all choices and print
any matches As luck would have it, the output is simply In other words,
the only number which fits the criteria is the one we found with our
brains alone:

<div style="text-align: center;">

> <span style="font-size: x-large;"><span class="katex"><span
> class="katex-inner"><span class="strut"
> style="height: 0.64444em;"></span><span
> class="strut bottom"></span><span
> class="base textstyle uncramped"><span class="mord">6</span><span
> class="mpunct">,</span><span class="mord">2</span><span
> class="mord">1</span><span class="mord">0</span><span
> class="mpunct">,</span><span class="mord">0</span><span
> class="mord">0</span><span class="mord">1</span><span
> class="mpunct">,</span><span class="mord">0</span><span
> class="mord">0</span><span
> class="mord">0</span></span></span></span></span>

</div>

This serves to make the interview question that much more difficult,
since there is a unique solution. [About Bossy
Lobster](https://profiles.google.com/114760865724135687241)

</p>

