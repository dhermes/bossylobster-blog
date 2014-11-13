title: Where have I been?
date: 2012-03-28
author: Danny Hermes (dhermes@bossylobster.com)
tags: App Engine, Google App Engine, Google Codesite, Open Source, Python, Stack Overflow
slug: where-have-i-been

Well, it's been a bit crazy and I haven't written a blog post in ages. I
have several brewing, but had just been too busy at work (and a ton of
travel for personal fun) to really have the excess time to write.

This return post will not have much content but will announce that I'm a
big boy now.

In the 1.6.3 release of the App Engine SDK (and hence runtime), three
nifty changes of mine were included. Two of them even made the
[Release Notes](http://code.google.com/p/googleappengine/wiki/SdkReleaseNotes#Version_1.6.3_-_February_28,_2012):

-   Code that inherits from the deferred library's `TaskHandler`
    can now define custom handling of exceptions.
    - See issue [6478](http://code.google.com/p/googleappengine/issues/detail?id=6478)
-   Fixed an issue so that a deferred task retries like a push queue task
    when using the `SingularTaskFailure` exception:
    - See issue [6412](http://code.google.com/p/googleappengine/issues/detail?id=6412)

In addition, the one that was most confusing to fix didn't make it into
any set of Release Notes, but I "closed" the
[issue](http://stackoverflow.com/questions/8304854/gql-query-with-key-in-list-of-keys)
that I originally opened on StackOverflow. Checkout the
[diff](http://code.google.com/p/googleappengine/source/diff?spec=svn241&r=241&format=side&path=/trunk/python/google/appengine/ext/gql/__init__.py&old_path=/trunk/python/google/appengine/ext/gql/__init__.py)
to see the details. I'll follow up with a summary of each of the fixes in a
later post.
