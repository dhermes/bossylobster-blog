Title: Protecting Sensitive Information in Public Git Repositories
Date: 2011-11-27 21:58
Author: Danny Hermes (noreply@blogger.com)
Tags: AppEngine, Commit Hook, Config Files, Git, Private Key, Protect, Python
Slug: protecting-sensitive-information-in-public-git-repositories

<p>
On the (much too early) bus to work this morning, I was reading my
Twitter feed and saw an [interesting
question](https://twitter.com/#!/robhawkes/status/121593545202216960) from
[Rob Hawkes](https://twitter.com/#!/robhawkes):  

<center>
<div id="post-container">

<div id="container-bg">

<div id="post-bg">

<span id="top-span"> <span id="follow-span"></span> <span
id="name-span"> [![Rob
Hawkes](http://www.bossylobster.com/images/blog/robhawkes.jpg)](http://twitter.com/intent/user?screen_name=robhawkes "Rob Hawkes")
**[@robhawkes](http://twitter.com/intent/user?screen_name=robhawkes "Rob Hawkes")**
<span style="color: #999999; font-size: 14px;">  
Rob Hawkes</span></span></span>   
<div style="margin: 1em 0em .5em 0em;">

How do you handle config files in your apps when you use Git? I keep
accidentally adding config files with sensitive data to Git. :(

</div>

<div style="font-size: 12px;">

[October 5, 2011 7:32
am](https://twitter.com/#!/robhawkes/status/121593545202216960 "tweeted on October 5, 2011 7:32 am")
via [TweetDeck](http://www.tweetdeck.com/)
[**Reply**](https://twitter.com/intent/tweet?in_reply_to=121593545202216960 "Reply")
[**Retweet**](https://twitter.com/intent/retweet?tweet_id=121593545202216960 "Retweet")
[**Favorite**](https://twitter.com/intent/favorite?tweet_id=121593545202216960 "Favorite")

</div>

</div>

</div>

</div>

</center>
Rob's Twitter followers made all kinds of recommendations and Rob
eventually decided it was a solved problem, declaring "Best method I've
found so far is creating a temporary config file and keeping that in
git, then .gitignoring the real one." and then "Thanks for the config
file tips! In the end I went with a "config.example.js" file stored in
[Git](http://git-scm.com/) and a "config.js" file that is ignored." For
those following along at home, they mean the same thing.  
  
As Rob was probably intending, this can be used for deploying an app on
your personal server, or for a sample App on a PaaS like [Google App
Engine](http://code.google.com/appengine/) or
[Heroku](http://www.heroku.com/). When testing such an app, the ability
to have a native environment locally is a huge convenience, but the
overhead of remembering which private keys need to be hidden is a
headache and sometimes completely neglected. But it shouldn't be,
because git never forgets!  
  
Anyone who has used git for any substantial amount of time probably
initially conceived of this hack when on first thought. (This is no
insult to Rob, just the inevitability of the pattern.) But, by the time
Rob posted his solution, I had moved on from this and came up a solution
that I think does the trick a bit more thoroughly. I envisioned a
solution which assumes people who checkout my code will want to keep
their config in a specified path that is already in the repo; of course,
I also wanted to share this with the interwebs.  
  
<span class="Apple-style-span">Anyhow, this is quick and dirty. First,
create <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js</span>
and <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js </span>in
the root directory of your git repository (the same directory that <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">.git</span>
lives in). I intend </span><span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js</span><span
class="Apple-style-span"> to be the local copy with my actual passwords
and keys and </span><span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js</span>to
hold the master contents that actually show up in the public repo. For
example, the contents of <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js
are</span>:  

<div style="text-align: center;">

<span class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">var
SECRET = 'Nnkrndkmn978489MDkjw';</span>

</div>

and the contents of <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js </span>are:  

<div style="text-align: center;">

<span class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">var
SECRET = 'SECRET';</span>

</div>

Since I ***don't*** want a duplicate in my repo, I put a rule in my
<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">.gitignore</span>
[file](http://progit.org/book/ch2-2.html#ignoring_files) to ignore <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js</span>.
(For those unfamiliar, this can be done just by including <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js </span>on
its own line in the <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">.gitignore </span>file.)
After doing so, I set up two [git
hooks](http://progit.org/book/ch7-3.html), a pre-commit and post-commit
hook.  
  
To "*install*" the hooks, just add the files <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">pre-commit </span>and <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">post-commit </span>to
the <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">.git/hooks</span>
subdirectory in your repo. They are nearly identical files, with a
one-line difference. Both files simply swap the contents of <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js</span><span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;"> </span>and <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js</span>,
while <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">pre-commit </span>also
adds <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js</span> to
the changelist. First I'll give you the contents of <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">pre-commit</span>,
and then explain why it's cool/safe:  

~~~~ {.prettyprint style="background-color: white;"}
#!/usr/bin/env pythonimport oshooks_dir = os.path.dirname(os.path.abspath(__file__))relative_dir = os.path.join(hooks_dir, '../..')project_root = os.path.abspath(relative_dir)git_included_config = os.path.join(project_root, 'config.js')confidential_config = os.path.join(project_root, '_config.js')with open(git_included_config, 'rU') as fh:  git_included_contents = fh.read()with open(confidential_config, 'rU') as fh:  confidential_contents = fh.read()with open(git_included_config, 'w') as fh:  fh.write(confidential_contents)with open(confidential_config, 'w') as fh:  fh.write(git_included_contents)os.system('git add %s' % git_included_config)
~~~~

(Also note the contents of <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">post-commit </span>are
exactly the same, except without the final statement: <span
class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">os.system('git
add %s' % git\_included\_config)</span>.)  
  
So what is happening in this file:  

1.  Uses the Python <span class="Apple-style-span"
    style="color: lime; font-family: 'Courier New', Courier, monospace;">os</span>
    module to determine the absolute path to the root directory in your
    project by using the absolute path of the hook file, backing up two
    directories and again find that absolute path.
2.  Determines the two files which need to swap contents
3.  Loads the contents into string variables and then writes them to the
    opposite files
4.  (only in <span class="Apple-style-span"
    style="color: lime; font-family: 'Courier New', Courier, monospace;">pre-commit</span>)
    Adds the included file to the changelist before the commit occurs.

Step 4 is actually the secret sauce. It puts cleaned, non-sensitive data
into the checked in <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js </span>file
and then updates the changelist before making a commit, to ensure only
the non-sensitive data goes in. Though you could do this yourself by
making an initial commit with clean data and then never <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">git
add</span>ing the file with your actual data, these hooks prevent an
accident and allow you to update your local <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js </span>file
with more fields as your config spec changes.  
  
But wait bossylobster, you say, what if one of the hooks doesn't occur?
You are right! As  <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">pre-commit </span>stands
above, if the changelist is empty we have problems. Since the pre-commit
hook changes  <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js</span> to
the same value in HEAD, git will tell us either "***nothing to
commit***" or "***no changes added to commit***". In this case, the
commit will exit and the post-commit hook will never occur. **<span
class="Apple-style-span" style="font-size: large;">This is very
bad</span>**, since the contents of <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">config.js </span>and <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_config.js </span>will
be switched but not switched back. So, to account for this, we need to
append the following code to the end of <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">pre-commit</span>:  

~~~~ {.prettyprint style="background-color: white;"}
with os.popen('git st') as fh:  git_status = fh.read()if ('nothing to commit' in git_status or    'no changes added to commit' in git_status or    'nothing added to commit' in git_status):  import sys  msg = '# From pre-commit hook: No commit necessary, ' \        'sensitive config unchanged. #'  hash_head = '#' * len(msg)  print ('%s\n%s\n%s\n\n' % (hash_head, msg, hash_head)),  with open(git_included_config, 'w') as fh:    fh.write(git_included_contents)  with open(confidential_config, 'w') as fh:    fh.write(confidential_contents)  sys.exit(1)
~~~~

For final versions see
the [pre-commit](http://www.bossylobster.com/scripts/pre-commit) and
[post-commit](http://www.bossylobster.com/scripts/post-commit) files.
Thanks again to [Rob Hawkes](https://twitter.com/#!/robhawkes) for the
idea/work break over lunch! [About Bossy
Lobster](https://profiles.google.com/114760865724135687241)  
  
**Update**: *One of Rob's followers, [Paul
King](https://twitter.com/#!/nrocy), found and
[tweeted](https://twitter.com/#!/nrocy/status/124468167086051328) a very
different alternative that is also pretty cool. Check out the
[post](http://archive.robwilkerson.org/2010/03/02/git-tip-ignore-changes-to-tracked-files/) he
found by [Rob Wilkerson](https://twitter.com/#!/robwilkerson).*  
  
**Update**: *I swapped out a screen shot of the tweet for a CSS-ified
version, inspired by and based on a design used on Mashable.*  
  
**Update**: *Some change in git causes empty commits to be allowed. I
either didn't notice this before or it just showed up in git. So I
added*<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">sys.exit(1)</span>*to
force the pre-commit script to fail when nothing is changed and added a
check for the phrase *<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">nothing
added to commit</span>*as well.*

</p>

