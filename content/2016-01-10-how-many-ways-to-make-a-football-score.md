title: How Many Ways to Make a (Football) Score
description: Describing all the ways a football score can be obtained
date: 2016-01-10
author: Danny Hermes (dhermes@bossylobster.com)
tags: Programming, JavaScript, Football
slug: how-many-ways-to-make-a-football-score
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/generic-football.png

While watching today's [Seahawks-Vikings game][1], my wife asked:

> How did the Seahawks score 9 points? Did they get a field goal
> and miss an extra point after a touchdown?

I had been head down coding and didn't know the answer. I quickly
jotted down the possibilities (like solving the
[coin-change problem][2] with coins of value 2, 3, 6, 7 and 8)
and told her it could be one of four outcomes:

- Field Goal (3), TD with missed PAT (6)
- 3 Field Goals (3 x 3)
- Safety (2), TD (7)
- 3 Safeties (3 x 2), Field Goal (3)

I decided it'd be fun to [make a tool][3] to answer this question
for any score (not just **9**). Enjoy

### Give me a score, I'll count the ways

<div>Score: <input type="text" id="num-points" name="numPoints" value="9" style="width: 35px; font-size: 18px;" onchange="bossylobsterBlog.FBScore.updatePage();"></div>
<ol id="scores-list">
  <li>1 x Field Goal, 1 x TD with missed PAT</li>
  <li>3 x Field Goal</li>
  <li>1 x Safety, 1 x TD</li>
  <li>3 x Safety, 1 x Field Goal</li>
</ol>

<script src="/js/scoring_possible.js" type="text/javascript"></script>

[1]: https://twitter.com/NFL_Memes/status/686293582672715778
[2]: https://en.wikipedia.org/wiki/Change-making_problem
[3]: https://gist.github.com/dhermes/c5088f4534108743015f
