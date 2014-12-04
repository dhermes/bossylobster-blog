title: Brand New Blog
date: 2014-12-03
author: Danny Hermes (dhermes@bossylobster.com)
tags: Pelican, Octopress, GitHub Pages
slug: brand-new-blog
comments: true

After a happy 3-year run with [Blogger][1], I've decided to
revamp my blog with viewers in mind.

## Why?

When I [started][3] my blog, I was still learning the ropes as a
programmer. I was happy to have a place to share the things I learned,
but didn't have much context for the things I was writing.
However, as I started to develop a voice, I became acutely aware
that the look and feel of my blog was bad.

After a good [friend][5] of mine asked me something along the lines
of "Danny, are you blind?", it was clear I needed to make a change.
He solidified what I had known for some time:

> In order to have a voice, I needed more than just content.

I needed to respect my viewers taste by providing a quality visual
experience. This was not clear to me as a freshly minted math nerd from
the University of Michigan.

However, after spending two and a half years at Google building plenty of
slide decks, I knew better. By not writing with viewers in mind, I was
weakening my work by increasing the effort required to consume it.

I hope you're enjoying a more visually pleasing blog
experience and welcome any [feedback][18] you may have.

Feel free to continue on if you are a nerd like me.

## How?

I am now hand-crafting HTML for my posts and using a static site
generator for my content. It feels so 90's, but I wasn't using the
internet then, so what do I know?

Inspired by my old buddy [Brian][6] and by the insanely productive
[Jake Vanderplas][7], I decided to port my old content by hand.

The current blog you see here is due to a few main ingredients:

- The [Pelican][2] static site generator, for the Python hacker in me.
- The [`octopress`][8] theme for Pelican. This is arguably the most
  important part. Big thanks to the [original][9] theme, I love it!
- Static content hosting via [GitHub Pages][10]. Luckily it's a breeze
  to [set up][12] a [custom domain][11].
- HTTPS always on and other perks from [CloudFlare][13]. They claim they
  only need five minutes and it is not an exaggeration!

Beyond that, I **enhanced** the Pelican dev experience by [adding][14]
a way to broadcast within my local network for local testing on
mobile devices. In addition, via [Travis][15], my blog has a [build][16]
stage just like real software. This allows the new static content
to be [built][17] every time I make a new commit to GitHub.

There were plenty of other fun hacks in the 150+ commits it took me
to make the switch, but I'll save that for another post.

[1]: http://bossylobster.blogspot.com/
[2]: http://docs.getpelican.com/en/latest/
[3]: https://blog.bossylobster.com/2011/04/first.html
[4]: https://blog.bossylobster.com/2014/09/quantitative-brain-teaser-brain-only.html
[5]: https://twitter.com/zacharykimball
[6]: http://brianmannmath.github.io/
[7]: https://jakevdp.github.io/blog/2013/05/07/migrating-from-octopress-to-pelican/
[8]: https://github.com/duilio/pelican-octopress-theme
[9]: http://octopress.org/
[10]: https://pages.github.com/
[11]: https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/
[12]: https://github.com/dhermes/dhermes.github.io/blob/master/CNAME
[13]: https://www.cloudflare.com/
[14]: https://github.com/dhermes/bossylobster-blog/commit/f578f3c70ea71f4e513c7ff10f5f5afc963b5df4
[15]: https://travis-ci.org/
[16]: https://github.com/dhermes/bossylobster-blog/blob/master/.travis.yml
[17]: https://travis-ci.org/dhermes/bossylobster-blog/
[18]: https://github.com/dhermes/bossylobster-blog/issues/new
