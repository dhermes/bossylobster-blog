---
title: Attack of Ruby Stack Traces
description: A short story from Bryan Cantrill about Twitter's fail whale
date: 2019-05-27
author: Danny Hermes (dhermes@bossylobster.com)
tags: Twitter, Programming, Ruby, Abstractions
slug: ruby-stack-traces
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/fail-whale.png
github_slug: content/2019-05-27-ruby-stack-traces.md
---

First, let me say I'm not posting this to shame any company or language
community. Getting to the scale Twitter reached in a short amount of time
can quickly make past engineering decisions look foolish in hindsight. But
almost always they are decisions made in good faith with the current
information.

Over the past 6 months, I've been trying my hardest to find an old talk I had
watched about a bug at Twitter that was responsible for the fail whale. I
**could not** find the talk for all I tried. When trying to find the talk, I
was searching for "memory leak" caused by "Ruby stack traces".

<div markdown="1" style="text-align: center;">
  ![Twitter Fail Whale](/images/fail-whale.png)
</div>

I couldn't find the talk for several reasons

- I thought the speaker was [Gary Bernhardt][1][ref]His talk
  [The Birth & Death of JavaScript][2] is so good[/ref] but it was actually
  [Bryan Cantrill][3]
- I was searching for "memory leak" but the issue was actually caused by
  excessive use of compute resources
- The comment was just a small footnote in a much longer talk about
  [The Summer of Rust][4]

When I finally found the talk, I was so excited. In order to make my future
Google searches actually turn up results I wanted to write this blog post.
Also, to make the searches a little more useful, please find the transcript
starting at the 26:30 mark[ref]Edited a
slight bit by removing some words such as "like"[/ref]:

> If you think Ruby's inefficient today ... Twitter was a big customer of ours
> and in 2007 I went into Twitter because &ndash; I feel like I'm the internet
> historian here &ndash; back in the day there was this thing called the fail
> whale on Twitter. Do you remember the fail whale? OK right.
>
> So Twitter would constantly keel over, you'd get like this whale that was
> indicating that things were awful and it was threatening the company. People
> wanted to not use Twitter as a result of this. Little did they know that
> there would be lots of other reasons to not use Twitter in the future but
> this is back when the actual the reliability of the thing was the biggest
> problem not like you know the Pepes or whatever.
>
> So we went into Twitter to try to help them understand what was going on and
> using [`dtrace`][5] to understand where it was spending time. I remember they
> were spending 460 milliseconds of compute for a request.
>
> > **Bryan Cantrill** "Do you mean microseconds?"
> >
> > **Twitter** "460 milliseconds"
> >
> > **Bryan Cantrill** "There's I/O. You're I/O bound."
> >
> > **Twitter** "No no we're not I/O bound. It's 100% compute bound."
> >
> > **Bryan Cantrill** "Are you sure that's right, that you're spending ... For
> > one request? **One request** would spend 460 milliseconds? Are you
> > sure ...?"
>
> But it was, it was milliseconds. Actually turns out what they were doing is
> kind of interesting and it shows the peril of language choices. They were
> spending all of their time in `bcopy()`, like 100% of their time in
> `bcopy()`. Why are they in `bcopy()`? They're in `bcopy()` because they are
> `bcopy()`-ing symbols out of their stack.
>
> Why are they doing this? Because
> they are deep deep deep in their Rails app and it was thought that to
> actually iterate over all the elements of an array from zero to the length
> the array &ndash; that's way too pedestrian, that's like repeating yourself
> or whatever. That's not DRY or whatever I don't even know what the Dogma was
> at the time. The "right" way to do this is to just blast through the array
> until you fall off the end and get an exception thrown at you. Exactly,
> you're like (brakes screeching sound) well you know it was ... anyway I don't
> know what to say about it.
>
> So what would happen is, it would go flying off the end of this array. It's
> like a four element array and it's hitting the fifth element and of course
> it's an exception and exceptions are really (should be) exceptional and when
> that exception is generated what Ruby would do is like "all right I now need
> to get a full stack back trace so you've got some hope in hell of figuring
> out where this random exception is" because the alternative is much worse.
> The alternative is like "something somewhere in there died and I got no idea
> where but we're now dead" so you don't want that, right? You want to have a
> stack backtrace.
>
> So it would walk up whatever it was, 434 stack frames and
> for each stack frame &ndash; and this is where you get to the point where
> it's like Ruby could be a little bit more efficient &ndash; for each stack
> frame it's looking up this symbol (and this kind of very inefficient
> mechanism for looking up a symbol) it would generate this huge string buffer,
> this 16K string buffer and it would: "alright time to get this ocean liner
> upstairs". It would kick that up to literally the caller of this thing "oh I
> got it that's fine I'm off the end of the array, no problem. I get it. But
> I've done it the right way! I've done it without repeating myself or
> whatever." (Facepalm)
>
> It's like "oh k". So that was obviously very bad. And it highlights a bunch
> of things. It highlights the cost of some of these abstractions, the runtime
> cost of some of these abstractions. How difficult it is to find these things
> when they misbehave that way. And how easy it is to abuse these things.

I've really enjoyed listening to both Bryan Cantrill and Gary Bernhardt talk
about software and I highly recommend watching **many** of their great talks.
Also it was super cool that when I finally [tweeted][6] about my search
for this old Twitter bug both Gary and Bryan interacted on Twitter!

[1]: https://twitter.com/garybernhardt
[2]: https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript
[3]: https://twitter.com/bcantrill
[4]: https://www.youtube.com/watch?v=YKv_IDN0zCA
[5]: http://dtrace.org/blogs/about/
[6]: https://twitter.com/bossylobster/status/1129873135132659714
