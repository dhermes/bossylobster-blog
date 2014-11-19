title: How to Lose Money in Vegas
date: 2014-11-18
author: Danny Hermes (dhermes@bossylobster.com)
tags:
slug: how-to-lose-money-in-vegas
comments: true

Or
<br />
<br />
<h1>What Dan Actually Knows About his Craps Strategy</h1>
<br />
For some insane reason, I enjoy making loans to Vegas casinos. My (current) favorite is the game of <a href="http://en.wikipedia.org/wiki/Craps">Craps</a>. It is widely known to be (close to) the <span style="outline: #0033ff solid;">best odds</span> of winning at a casino.
<br />
<br />
However, many people make silly bets at the table because they have fun. From time to time, I am one of those silly bettors. Since I like the rush of occasionally <span style="outline: #0033ff solid;">winning 7 or 9 times</span> my bet, I play a side bet called the "Hard Ways" <a href="https://www.youtube.com/watch?v=OftDvIJYxKk#t=24s">bet</a>. I'm aware these bets live on a part of the Craps table referred to as sucker bets; this makes sense &mdash; the bet <span style="outline: #0033ff solid;">loses 40 cents of every dollar</span> (in expectation).
<br />
<hr />
<h3>Let's Do Some Math</h3>
<br />
<br />
<div class="separator" style="clear: both; text-align: center;"><a href="http://2.bp.blogspot.com/-mDwr5iYMmpc/U_v-ymatQqI/AAAAAAAAP4Q/j_oZunoGZck/s1600/IMG_2042.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="http://2.bp.blogspot.com/-mDwr5iYMmpc/U_v-ymatQqI/AAAAAAAAP4Q/j_oZunoGZck/s400/IMG_2042.png" /></a></div>
<br />
<br />
<br />
<br />
http://mathb.in/4691<br />
<br />
<br />
I was recently playing a silly strategy in Craps and was curious what my expected payouts were. I did a fair amount of stupid math (that ended up having bad assumptions) but eventually found my way. I thought a few of the calculations were fun, so I've included them here.

First, some bits of notation and definitions:
<br />
<ul>
<li>\(P = \left\{4, 5, 6, 8, 9, 10\right\}\) the set of points which can be established</li>
<li>\(T = \left\{4, 6, 8, 10\right\}\) the set of hard way totals which can be bet on</li>
<li>\(\text{EP}(p)\) the expected payout of playing the strategy when the point has been set at \(p\) (since a hard-way can only be played once a point has been set, we must start with a point set)</li>
<li>The operator \(\text{Pr}\) to denote the probability of an event occurring</li>
<li>The operator \(\text{E}\) to denote the expected value of a random variable</li>
<li>\(\text{NWR}(p)\) the number of ways to roll a point \(p\)</li>
<li>\(W_p\) the event that a turn rolling with point \(p\) results in winning the point</li>
<li>\(L_p\) the random variable representing the length of the game once the point is set at \(p\)</li>
<li>\(w_t\) the weight or payout of rolling a hard \(t\) (typically these values are \(w_4 = w_{10} = 7\) and \(w_6 = w_8 = 9\), but we need not make any assumptions for our calculations)</li>
<li>\(H_{t, p}\) the random variable representing the number of hard way rolls of the total \(t\) during a turn when the point is set at \(p\)</li>
<li>\(E_{t, p}\) defined similarly as \(H_{t,p}\) but for easy way rolls</li>
<li>\(\$1\) the amount placed on each hard way bet (or \(1\) unit of any other currency you like)
</li>
</ul>
To compute the values \(\text{EP}(p)\) for all points \(p \in P\) we will compute

\[ \text{EP}(p) = \left[ \sum_{t \in T} w_t \cdot \text{E}(H_{t, p}) \right] - \left[ \sum_{t \in T} \text{E}(E_{t, p}) \right] - 4 \cdot \text{Pr}\left(W_p^C\right). \]

The first term is the total expected pay, which is simply the weighted sum of the expected number of hard rolls for each total \(t \in T\), weighted by their payouts. The second term is the expected loss over the life of a roll, since each time an easy way roll occurs, the bet (with value \(1\)) needs to be replaced. Finally, the last term, is the expected loss from a term ending in \(7\) out, since in that case all \(4\) bets on the hard ways will be lost to the house.

It remains to compute these component parts.

<br />
<h2>
\(\text{Pr}(W_p)\)</h2>
Ostensibly, it would seem that we need to calculate

\[ \text{Pr}(W_p) = \sum_{L = 1}^{\infty} \text{Pr}(W_p \, \mid \, L_p = L) \cdot \text{Pr}(L_p = L). \]

As it turns out \(\text{Pr}(W_p \, \mid \, L_p = L)\) is independent of \(L\) and since \( \sum_{L = 1}^{\infty} \text{Pr}(L_p = L) \) must be equal to \(1\), we have \(\text{Pr}(W_p) = \text{Pr}(W_p \, \mid \, L_p = L)\) for any \(L\) (so long as we can show these values to be independent of \(L\)).

<strong>NOTE:</strong> This calculation tripped me up <em>so</em> many times; I had to run a big simulation to convince me of the correct answer and fix my wrong headed approach.

We must have

\[  \text{Pr}(W_p \, \mid \, L_p = L) = \frac{\prod_{i =1}^L N_i}{\prod_{i =1}^L N_i'} \]

where \(N_i\) is the number of values roll \(i\) can take if the turn (with point set at \(p\)) has length \(L\) and ends in a win and \(N_i'\) is the number of values roll \(i\) can take simply if the turn has length \(L\) and ends in any way at all.

Since it must have length \(L\), for \(i &lt; L\) we know that roll \(i\) can be anything except the point or a \(7\), hence

\[ N_i = N_i' = 36 - \text{NWR}(p) - \text{NWR}(7). \]

This reduces the ratio of products to

\[  \text{Pr}(W_p \, \mid \, L_p = L) = \frac{N_L}{N_L'}  = \frac{\text{NWR}(p)}{\text{NWR}(p) + \text{NWR}(7)} \]

where \(N_L = \text{NWR}(p)\) since a win can only occur on roll \(L\) if the point \(p\) is rolled and \(N_L' = \text{NWR}(p) + \text{NWR}(7)\) since either the point \(p\) or a \(7\) must be rolled to end the turn on roll \(L\).

Noting that \(\text{NWR}(7) = 6\), we have

\[ \text{Pr}(W_p) = \frac{\text{NWR}(p)}{\text{NWR}(p) + 6} \]

<br />
<h2>
\(\text{E}(H_{t, p})\)</h2>
In the case that \(t \neq p\), hard totals are independent of the length since they don't end the game, hence

\[ \text{E}(H_{t, p}) = \text{E}(H_t) \cdot \text{E}(L_p) \]

where \(H_t\) is the indicator random variable representing whether a single roll is a hard \(t\). Since a hard total can only occur once and \(H_t\) is just an indicator, we have \(\text{E}(H_t) = \frac{1}{36}\), the probability of the event.

<br />
<hr />
<h3>
\(\text{E}(L_p)\)</h3>
Let \(F_p\) be the event that the first roll is "final", i.e. it ends the turn, so is either \(p\) or \(7\). We know that

\[ \text{E}(L_p) = \text{E}(L_p \, \mid \, F_p) \cdot \text{Pr}(F_p) + \text{E}\left(L_p \, \mid \, F_p^C \right) \cdot \text{Pr}\left(F_p ^C \right). \]

Since \(F_p\) ends the turn and \(F_p^C\) simply continues it, we have \(\text{E}(L_p \, \left\vert\right. \, F_p) = 1\) and \(\text{E}\left(L_p \, \mid \, F_p^C \right) = 1 + \text{E}(L_p)\). Using this,

\begin{align*}
\text{E}(L_p) &amp;= 1 \cdot \text{Pr}(F_p) + \left(1 + \text{E}(L_p)\right) \cdot \left(1 - \text{Pr}\left(F_p \right)\right) \\
&amp;= \text{Pr}(F_p) + 1 - \text{Pr}\left(F_p \right) + \text{E}(L_p) - \text{Pr}\left(F_p \right) \cdot \text{E}(L_p) \\
&amp;= 1 + \text{E}(L_p) - \text{Pr}\left(F_p \right) \cdot \text{E}(L_p) \\
\Rightarrow 0 &amp;= 1 - \text{Pr}\left(F_p \right) \cdot \text{E}(L_p) \\
\Rightarrow \text{E}(L_p) &amp;= \frac{1}{\text{Pr}\left(F_p \right)} .
\end{align*}

To simplify this, note that \(\text{Pr}\left(F_p \right) = \frac{\text{NWR}(p)}{36} + \frac{\text{NWR}(7)}{36}\) hence

\[ \text{E}(L_p) = \frac{36}{\text{NWR}(p) + 6}. \]

<br />
<hr />
So, when \(t \neq p\), we have

\[ \text{E}(H_{t, p}) = \frac{1}{36} \cdot \frac{36}{\text{NWR}(p) + 6} = \frac{1}{\text{NWR}(p) + 6}. \]

When \(t = p\), rolling a hard way also means ending the game, so it is not independent from the length. In this case,

\[ \text{E}(H_{t, p}) = \text{E}(H_{t, p} \, \left\vert\right. \, W_p) \cdot \text{Pr}(W_p) + \text{E}\left(H_{t, p} \, \left\vert\right. \, W_p^C\right) \cdot \text{Pr}\left(W_p^C\right). \]

Since \(W_p^C\) (not winning the turn) implies \(p\) was never rolled, we know \(\text{E}\left(H_{t, p} \, \left\vert\right. \, W_p^C\right) = 0\). Since rolling a single \(p\) will end the turn with either \(0\) or \(1\) hard way rolls of \(t = p\),

\[ \text{E}(H_{t, p} \, \left\vert\right. \, W_p) = 1 \cdot \text{Pr}(\text{WRH} \, \left\vert\right. \, W_p) + 0 \cdot \text{Pr}\left(\text{WRH}^C \, \left\vert\right. \, W_p\right) \]

where \(\text{WRH}\) is the event that the winning roll is a hard way. But \(\text{Pr}(\text{WRH} \, \left\vert\right. \, W_p)\) can be computed irrespective of length in the same fashion that \(\text{Pr}(W_p)\) was:

\[ \text{Pr}(\text{WRH} \, \mid \, W_p) = \frac{1}{\text{NWR}(p)} \]

since exactly \(1\) roll is a hard way while \(\text{NWR}(p)\) of them will end the turn in a win.

Plugging this back in, we have

\begin{align*}
\text{E}(H_{t, p}) &amp;= \text{Pr}(\text{WRH} \, \left\vert\right. \, W_p) \cdot \text{Pr}(W_p) + 0 \cdot \text{Pr}\left(W_p^C\right) \\
&amp;= \frac{1}{\text{NWR}(p)} \cdot \frac{\text{NWR}(p)}{\text{NWR}(p) + 6} \\
&amp;= \frac{1}{\text{NWR}(p) + 6}
\end{align*}

and see the value is fully independent of \(t\).

<br />
<h2>
\(\text{E}(E_{t, p})\)</h2>
In both cases \(t = p\) and \(t \neq p\), the calculations for \(E_{t, p}\) are very similar to those for \(H_{t, p}\).

In the case that \(t \neq p\), easy totals are also independent of the length, hence

\[ \text{E}(E_{t, p}) = \text{E}(E_t) \cdot \text{E}(L_p) \]

where \(E_t\) is the indicator random variable representing whether a single roll is an easy \(t\). As with hard totals, \(\text{E}(E_t) = \frac{\text{NWR}(t) - 1}{36}\) since \(\text{NWR}(t) - 1\) of the \(\text{NWR}(t)\) rolls of \(t\) are <em>not</em> hard rolls.

This means

\[ \text{E}(E_{t, p}) = \frac{\text{NWR}(t) - 1}{36} \cdot \frac{36}{\text{NWR}(p) + 6} = \frac{\text{NWR}(t) - 1}{\text{NWR}(p) + 6}. \]

In the case that \(t = p\), we have the similar equalities.

\[ \text{E}(E_{t, p}) = \text{E}(E_{t, p} \, \left\vert\right. \, W_p) \cdot \text{Pr}(W_p) + \text{E}\left(E_{t, p} \, \left\vert\right. \, W_p^C\right) \cdot \text{Pr}\left(W_p^C\right). \]

where again \(\text{E}\left(E_{t, p} \, \left\vert\right. \, W_p^C\right) = 0\). Another similar piece of logic yields:

\[ \text{E}(E_{t, p} \, \left\vert\right. \, W_p) = 0 \cdot \text{Pr}(\text{WRH} \, \left\vert\right. \, W_p) + 1 \cdot \text{Pr}\left(\text{WRH}^C \, \left\vert\right. \, W_p\right) \]

where we switch the \(0\) and \(1\) since we are now counting an easy way roll, not a hard way.

Hence

\[ \text{E}(E_{t, p} \, \left\vert\right. \, W_p) = 1 - \text{Pr}(\text{WRH} \, \left\vert\right. \, W_p) = \frac{\text{NWR}(p) - 1}{\text{NWR}(p)} = \frac{\text{NWR}(t) - 1}{\text{NWR}(p)} \]

since \(t = p\). Plugging this back in, we have

\begin{align*}
\text{E}(E_{t, p}) &amp;= \text{Pr}\left(\text{WRH}^C \, \left\vert\right. \, W_p\right) \cdot \text{Pr}(W_p) + 0 \cdot \text{Pr}\left(W_p^C\right) \\
&amp;= \frac{\text{NWR}(t) - 1}{\text{NWR}(p)} \cdot \frac{\text{NWR}(p)}{\text{NWR}(p) + 6} \\
&amp;= \frac{\text{NWR}(t) - 1}{\text{NWR}(p) + 6}
\end{align*}

so this value is independent of whether \(t = p\) or not.

<br />
<h2>
Final Computation</h2>
Using the values for \(\text{E}(H_{t, p})\) and \(\text{E}(E_{t, p})\), we have

\[  \sum_{t \in T} w_t \cdot \text{E}(H_{t, p}) = \frac{1}{\text{NWR}(p) + 6} \cdot \sum_{t \in T} w_t \]

and

\[ \sum_{t \in T} \text{E}(E_{t, p}) = \frac{1}{\text{NWR}(p) + 6} \cdot \sum_{t \in T} (\text{NWR}(t) - 1) = \frac{3  - 1 + 5  - 1 + 5  - 1 + 3  - 1}{\text{NWR}(p) + 6} = \frac{12}{\text{NWR}(p) + 6}. \]

Stitching this all together:

\begin{align*}
\text{EP}(p) &amp;= \left[ \sum_{t \in T} w_t \cdot \text{E}(H_{t, p}) \right] - \left[ \sum_{t \in T} \text{E}(E_{t, p}) \right] - 4 \cdot \text{Pr}\left(W_p^C\right) \\
&amp;= \frac{\sum_{t \in T} w_t}{\text{NWR}(p) + 6} - \frac{12}{\text{NWR}(p) + 6} - 4 \cdot \left(1 - \frac{\text{NWR}(p)}{\text{NWR}(p) + 6}\right) \\
&amp;= \frac{\left[\sum_{t \in T} w_t\right] - 12}{\text{NWR}(p) + 6} - 4 \cdot \frac{6}{\text{NWR}(p) + 6} \\
&amp;= \frac{\left[\sum_{t \in T} w_t\right] - 36}{\text{NWR}(p) + 6}.
\end{align*}

<br />
<h2>
Overall Expectation</h2>
To compute a generic value \(\text{EP}\) for arbitrary choice of \(p\), we need to compute

\[ \text{EP} = \sum_{p \in P} \text{EP}(p) \cdot \text{Pr}(P_p) \]

where \(P_p\) is the event that the point is set at \(p\). Since there are

\[ \sum_{p \in P} \text{NWR}(p) = 3 + 4 + 5 + 5 + 4 + 3 = 24 \]

rolls which set a point, we simply have \(\text{Pr}(P_p) = \frac{\text{NWR}(p)}{24}\).

Denoting \(K = \left[\sum_{t \in T} w_t\right] - 36\), we have

\begin{align*}
\text{EP} &amp;= \frac{K}{9} \cdot \frac{3}{24} + \frac{K}{10} \cdot \frac{4}{24} + \frac{K}{11} \cdot \frac{5}{24} + \frac{K}{11} \cdot \frac{5}{24} + \frac{K}{10} \cdot \frac{4}{24} + \frac{K}{9} \cdot \frac{3}{24} \\
&amp;= \frac{K}{9} \cdot \frac{1}{4} + \frac{K}{10} \cdot \frac{1}{3} + \frac{K}{11} \cdot \frac{5}{12} \\
&amp;= \frac{55 \cdot K}{55 \cdot 9 \cdot 4} + \frac{66 \cdot K}{66 \cdot 10 \cdot 3} + \frac{15 \cdot 5 \cdot K}{15 \cdot 11 \cdot 12} \\
&amp;= \frac{196 \cdot K}{1980} \\
&amp;= \frac{49 \cdot K}{495} \\
&amp;= \frac{49 \cdot \left(\left[\sum_{t \in T} w_t\right] - 36\right)}{495}
\end{align*}

<br />
<h2>
Standard Payouts</h2>
In the standard case that \(w_4 = w_{10} = 7\) and \(w_6 = w_8 = 9\), we have \(\sum_{t \in T} w_t = 2 \cdot (7 + 9) = 32\), so

\[ \text{EP}(p) = - \frac{4}{\text{NWR}(p) + 6}. \]

This gives

\begin{align*}
\text{E}(4) &amp;= \text{E}(10) = - \frac{4}{9} = - 0.\overline{4}\\
\text{E}(5) &amp;= \text{E}(9) = - \frac{4}{10} = - 0.4 \\
\text{E}(6) &amp;= \text{E}(8) = - \frac{4}{11} = - 0.\overline{36} \\
\text{EP} &amp;= \frac{49 \cdot (-4)}{495} = - \frac{196}{495} = - 0.3\overline{95}.
\end{align*}
<br />
<br />
<br />
CODE SNIPPETS:<br />
https://docs.google.com/file/d/0B8el7dRo8mVOc2p1Y0MzSF9sZjg/edit
