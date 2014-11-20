title: TBD
date: 2014-11-20
author: Danny Hermes (dhermes@bossylobster.com)
tags:
slug: fix-dirty-branch
comments: true

```
$ git checkout --detach HEAD
...
$ git branch
* (detached from HEAD)
  master
$ git branch -m master master-dirty
$ git branch
* (detached from HEAD)
  master-dirty
$ git branch master origin/master
Branch master set up to track remote branch master from origin.
$ git branch
* (detached from HEAD)
  master
  master-dirty
$ git checkout master
$ git branch
* master
  master-dirty
$ git merge --squash master-dirty
Updating ffffff3..beeabee
Fast-forward
...
$ git branch -D master-dirty
Deleted branch master-dirty (was beeabee).
```
