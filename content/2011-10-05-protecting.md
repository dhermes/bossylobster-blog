title: Protecting Sensitive Information in Public Git Repositories
date: 2011-10-05
author: Danny Hermes (dhermes@bossylobster.com)
tags: App Engine, Commit Hook, Config Files, Git, Private Key, Protect, Python
slug: protecting
comments: true

On the (much too early) bus to work this morning, I was reading my
Twitter feed and saw an
[interesting question](https://twitter.com/#!/robhawkes/status/121593545202216960)
from [Rob Hawkes](https://twitter.com/#!/robhawkes):

<center>
  <div id="post-container">
    <div id="container-bg">
      <div id="post-bg">
        <span id="top-span">
          <span id="follow-span">
            <iframe allowtransparency="true" frameborder="0" scrolling="no" src="http://platform.twitter.com/widgets/follow_button.html#_=1319487235961&amp;align=right&amp;button=blue&amp;id=twitter_tweet_button_2&amp;lang=en&amp;link_color=%230084B4&amp;screen_name=robhawkes&amp;show_count=false&amp;show_screen_name=&amp;text_color="></iframe>
          </span>
          <span id="name-span">
            <a class="anchor-twitter" href="http://twitter.com/intent/user?screen_name=robhawkes" title="Rob Hawkes">
              <img alt="Rob Hawkes" id="id-img" src="/images/robhawkes.jpg" />
            </a>
            <strong>
              <a class="anchor-twitter" href="http://twitter.com/intent/user?screen_name=robhawkes" style="color: #0084b4;" title="Rob Hawkes">@robhawkes</a>
            </strong>
            <span style="color: #999999; font-size: 14px;"><br />Rob Hawkes</span>
          </span>
        </span>
        <br />
        <div style="margin: 1em 0em .5em 0em;">How do you handle config files in your apps when you use Git? I keep accidentally adding config files with sensitive data to Git. :(
        </div>
        <div style="font-size: 12px;">
          <a class="anchor-twitter" href="https://twitter.com/#!/robhawkes/status/121593545202216960" style="color: #0084b4;" target="_blank" title="tweeted on October 5, 2011 7:32 am">October 5, 2011 7:32 am</a>
          via
          <a class="anchor-twitter" href="http://www.tweetdeck.com/" rel="nofollow" style="color: #0084b4;" target="blank">TweetDeck</a>
        </div>
      </div>
    </div>
  </div>
</center>

Rob's Twitter followers made all kinds of recommendations and Rob
eventually decided it was a solved problem, declaring

> Best method I've found so far is creating a temporary config file and
> keeping that in `git`, then `.gitignore`ing the real one.

and then

> Thanks for the config file tips! In the end I went with a `config.example.js`
> file stored in [`git`](http://git-scm.com/) and a `config.js` file that is
> ignored.

For those following along at home, they mean the same thing.

As Rob was probably intending, this can be used for deploying an app on
your personal server, or for a sample App on a PaaS like
[Google App Engine](http://code.google.com/appengine/) or
[Heroku](http://www.heroku.com/). When testing such an app, the ability
to have a native environment locally is a huge convenience, but the
overhead of remembering which private keys need to be hidden is a
headache and sometimes completely neglected. But it shouldn't be,
because `git` never forgets!

Anyone who has used `git` for any substantial amount of time probably
initially conceived of this hack when on first thought. (This is no
insult to Rob, just the inevitability of the pattern.) But, by the time
Rob posted his solution, I had moved on from this and came up a solution
that I think does the trick a bit more thoroughly. I envisioned a
solution which assumes people who checkout my code will want to keep
their config in a specified path that is already in the repo; of course,
I also wanted to share this with the interwebs.

Anyhow, this is quick and dirty. First, create `config.js` and `_config.js`
in the root directory of your git repository (the same directory that `.git/`
lives in). I intend `config.js` to be the local copy with my actual passwords
and keys and `_config.js` to hold the master contents that actually show up in
the public repo. For example, the contents of `config.js` are:

```javascript
var SECRET = 'Nnkrndkmn978489MDkjw';
```

and the contents of `_config.js`
are:

```javascript
var SECRET = 'SECRET';
```

Since I **don't** want a duplicate in my repo, I put a rule in my `.gitignore`
[file](http://progit.org/book/ch2-2.html#ignoring_files) to ignore `_config.js`.
(For those unfamiliar, this can be done just by including `_config.js` on its
own line in the `.gitignore` file.) After doing so, I set up two
[git hooks](http://progit.org/book/ch7-3.html), a pre-commit and post-commit
hook.

To **install** the hooks, just add the files `pre-commit` and `post-commit`
to the `.git/hooks/` subdirectory in your repo.They are nearly identical files,
with a one-line difference. Both files simply swap the contents of `config.js`
and `_config.js`, while `pre-commit` also adds `config.js` to the changelist.
First I'll give you the contents of `pre-commit`, and then explain why it's
cool/safe:

```python
#!/usr/bin/env python

import os

hooks_dir = os.path.dirname(os.path.abspath(__file__))
relative_dir = os.path.join(hooks_dir, '../..')
project_root = os.path.abspath(relative_dir)

git_included_config = os.path.join(project_root, 'config.js')
confidential_config = os.path.join(project_root, '_config.js')

with open(git_included_config, 'rU') as fh:
  git_included_contents = fh.read()

with open(confidential_config, 'rU') as fh:
  confidential_contents = fh.read()

with open(git_included_config, 'w') as fh:
  fh.write(confidential_contents)

with open(confidential_config, 'w') as fh:
  fh.write(git_included_contents)

os.system('git add %s' % git_included_config)
```

Also note the contents of `post-commit` are exactly the same, except without
the final statement:

```python
os.system('git add %s' % git_included_config).
```

So what is happening in this file:

1.  Uses the Python `os` module to determine the absolute path to the root
    directory in your project by using the absolute path of the hook file,
    backing up two directories and again find that absolute path.
1.  Determines the two files which need to swap contents
1.  Loads the contents into string variables and then writes them to the
    opposite files
1.  (only in `pre-commit`) Adds the included file to the changelist before
    the commit occurs.

Step 4 is actually the secret sauce. It puts cleaned, non-sensitive data
into the checked in `config.js` file and then updates the changelist before
making a commit, to ensure only the non-sensitive data goes in. Though you
could do this yourself by making an initial commit with clean data and then
never `git add`ing the file with your actual data, these hooks prevent an
accident and allow you to update your local `_config.js` file with more
fields as your config spec changes.

But wait bossylobster, you say, what if one of the hooks doesn't occur?
You are right! As `pre-commit` stands above, if the changelist is empty we
have problems. Since the pre-commit hook changes `config.js` to the same
value in `HEAD`, `git` will tell us either **nothing to commit** or
**no changes added to commit**. In this case, the commit will exit and the
post-commit hook will never occur. **THIS IS VERY BAD**, since the contents of
`config.js` and `_config.js` will be switched but not switched back. So, to
account for this, we need to append the following code to the end of
`pre-commit`:

```python
with os.popen('git st') as fh:
  git_status = fh.read()

if ('nothing to commit' in git_status or
    'no changes added to commit' in git_status or
    'nothing added to commit' in git_status):
  import sys

  msg = ('# From pre-commit hook: No commit necessary, '
         'sensitive config unchanged. #')
  hash_head = '#' * len(msg)
  print ('%s\n%s\n%s\n\n' % (hash_head, msg, hash_head)),

  with open(git_included_config, 'w') as fh:
    fh.write(git_included_contents)

  with open(confidential_config, 'w') as fh:
    fh.write(confidential_contents)

  sys.exit(1)
```

For final versions see the
[pre-commit](https://gist.github.com/dhermes/21b152c25a321b554b61) and
[post-commit](https://gist.github.com/dhermes/877ed7c9838d6fc5bb08)
files. Thanks again to [Rob Hawkes](https://twitter.com/#!/robhawkes)
for the idea/work break over lunch!

#### Update 1:

One of Rob's followers, [Paul King](https://twitter.com/#!/nrocy), found and
[tweeted](https://twitter.com/#!/nrocy/status/124468167086051328) a very
different alternative that is also pretty cool. Check out the
[post](http://archive.robwilkerson.org/2010/03/02/git-tip-ignore-changes-to-tracked-files/)
he found by [Rob Wilkerson](https://twitter.com/#!/robwilkerson).

#### Update 2:

I swapped out a screen shot of the tweet for a CSS-ified
version, inspired by and based on a design used on Mashable.

#### Update 3:

Some change in `git` causes empty commits to be allowed. I either didn't
notice this before or it just showed up in `git`. So I added `sys.exit(1)`
to force the pre-commit script to fail when nothing is changed and added
a check for the phrase **nothing added to commit** as well.

<style type="text/css">
  a.anchor-twitter, a:visited.anchor-twitter {
    font-weight: bolder;
    font-style: normal;
    text-decoration: none;
    outline: none;
  }

  iframe {
    width: 300px;
    height: 20px;
  }

  .bump-left {
    margin-left: 1em;
  }

  #post-container {
    font: 14px/1.231 helvetica,arial,clean,sans-serif;
    display: inline-block;
    position: relative;
    width: 640px;
    text-align: left;
  }

  #container-bg {
    background: url(/images/twitter-bg.png) no-repeat #EBEBEB;
    padding: 20px;
    margin: 8px 0;
  }

  #post-bg {
    background: #fff;
    color: #000;
    padding: 10px 12px 2px 12px;
    margin: 0;
    min-height: 60px;
    font-size: 18px;
    line-height: 22px;
    -moz-border-radius: 5px;
    -webkit-border-radius:5px;
    -moz-box-shadow:0 2px 2px rgba(0,0,0,0.2);
    -webkit-box-shadow:0 2px 2px rgba(0,0,0,0.2);
    box-shadow:0 2px 2px rgba(0,0,0,0.2);
  }

  #top-span {
    width: 100%;
    margin-bottom: 12px;
    padding-top: 8px;
    height: 40px;
  }

  #follow-span {
    float: right;
    width: 300px;
    font-size: 12px;
    text-align: right;
  }

  #name-span {
    line-height: 19px;
  }

  #id-img {
    float: left;
    margin: 0px 7px 0px 0px;
    width: 38px;
    height: 38px;
    padding: 0;
    border: none;
  }
</style>
