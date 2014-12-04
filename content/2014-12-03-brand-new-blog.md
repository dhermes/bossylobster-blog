title: Brand New Blog
date: 2014-12-03
author: Danny Hermes (dhermes@bossylobster.com)
tags: Pelican, Octopress, GitHub Pages
slug: brand-new-blog
comments: true

After a happy 3-year run with [blogger][1], I've taken the plunge.
I am now hand-crafting HTML for my posts and using a static site
generator for my content. It feels so 90's, but I didn't know
anything about the internet then, so maybe not quite.

## Why?

When I [started][3] my blog, I was still a greenhorn. I was happy to
have a place to share the things I learned, but still had plenty to
learn. However, as I started to develop a voice, I became acutely aware
that the look and feel of my blog was not good.

It came to a head when I wanted to make some parts stand out in
a [post][4] about an interview brain teaser. A good [friend][5] of mine
took me to task; it was something along the lines of "Danny, this
looks like shit".

He solidified what I had known for some time:

> In order to have a voice, I needed more than just content.

I needed to respect my viewers taste in a quality viewing experience.
As a freshly minted math nerd from the University of Michigan, I had
no appreciation for the look and feel of things. However, after two
and a half years in a job that required plenty of public speaking,
it became clear that the presentation of a message has a large impact
on its reception.

Thanks for reading! Feel free to continue on if you are a
nerd like me.

## How?

Inspired by my old pal [Brian][6] and by the insanely productive
[Jake Vanderplas][7], I decided to port my old content by hand.

The current blog you see here is due to a few main ingredients:

-   The [Pelican][2] static site generator, for the Python hacker in me.
-   The [`octopress`][8] theme for Pelican. This is arguably the most
    important part. Big thanks to the [original][9] theme, I love it!
-   Static content hosting via [GitHub Pages][10]. Luckily it's a breeze
    to [set up][12] a [custom domain][11].
-   HTTPS always on and other perks from [CloudFlare][13]. Their slogan

    > "Give us five minutes and we'll supercharge your website."

    is spot on; CloudFlare is so easy to use!

Beyond that, I "enhanced" the Pelican dev experience by [adding][14]
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
