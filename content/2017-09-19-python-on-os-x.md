title: Installing Python on OS X
description: The Hows and Whys of Python versions
date: 2017-09-19
author: Danny Hermes (dhermes@bossylobster.com)
tags: Programming, Mac OS X, Python, pyenc
slug: python-on-os-x
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/python-logo.png
github_slug: content/2017-09-19-python-on-os-x.md

> **Caveat**: I stopped using a Mac for my development machine way
> back in the fall of 2014. You probably shouldn't listen to me.

### What Not to Do

The first rule of using Python on any operating system: **don't use
system Python**. The OS **relies** on that Python, including the packages
(and package versions) it has installed. This means if it is modified in a
non-official way by you, then the OS may not have something it depends on.

For Mac OS X, system Python is installed in

```
/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python
```

(YMMV, this is on a "current"-ish OS X 10.11.6). You couldn't edit it if
you wanted to &mdash; not even with `sudo` &mdash; it's [restricted][8].

Instead, most choose one of

* the [pyenv][3] version manager
* a custom Python from [Homebrew][4]
* the [conda][7] package management system
* "official" Python directly from [Python.org][6]

### What To Do

I **strongly** recommend using `pyenv`. Once installed and configured it
allows easy switching between versions and more importantly allows you
to have all versions owned by you (not `root`) and in one easy to find
(and easy to remove) place.

For example, the system Python is `2.7.10` and was compiled with LLVM 7.0.0:

```
$ /System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7 -c \
>   'import sys; print(sys.version)'
2.7.10 (default, Oct 23 2015, 19:19:21)
[GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.59.5)]
```

However, with `pyenv` installed, we can use the latest[ref]2.7.14 came out
only a few days before this post[/ref] version of 2.7[ref]I would like
to [encourage][10] you to use Python 3, and am just using 2.7 here
because that is the system Python[/ref]:

```
$ python2.7
Python 2.7.14 (default, Sep 19 2017, 20:32:14)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.executable
'${HOME}/.pyenv/versions/2.7.14/bin/python'
```

Multiple Python executables live peacefully together:

```
$ python -c 'import sys; print(sys.executable)'
${HOME}/.pyenv/versions/3.6.2/bin/python
$ python3.5 -c 'import sys; print(sys.executable)'
${HOME}/.pyenv/versions/3.5.4/bin/python3.5
```

When compared with the ease of `pyenv install ${VERSION}` without any root
privileges, downloading a `.pkg` from Python.org and running as administrator
seems unnecessary. However, I recently found a reason why the "official"
OS X Python binaries are worth having.

### Spinning Wheels

I decided I should be a "good citizen" and provide built Python
wheels for a [package][5] of mine. Along the process, I came across
[Matthew Brett][2]'s wonderful [Spinning Wheels][1].

TL;DR: it's best to build wheels that target OS X with the Python
executables from Python.org.

The primary difference between a `pyenv` installed Python and an official
one can be seen in the platform tag:

```
$ cat get_platform.py
import distutils.util
print(distutils.util.get_platform())
$ ${HOME}/.pyenv/versions/3.6.2/bin/python get_platform.py
macosx-10.11-x86_64
$ /Library/Frameworks/Python.framework/Versions/3.6/bin/python3 get_platform.py
macosx-10.6-intel
```

First, the Python.org Python[ref]The one that starts with `/Library/...`[/ref]
supports an older SDK (10.6) which gives **forward compatibility** of any
binaries produced for any SDK after 10.6.

Second, the `intel` architecture means the executable is a [universal][11]
(or "fat") binary. This means it can support both [32-bit][12] and 64-bit
architectures:

```
$ cd /Library/Frameworks/Python.framework/Versions/3.6/bin/
$ ./python3
>>> import sys
>>> sys.maxsize
9223372036854775807
>>> sys.maxsize == 2**(64 - 1) - 1
True
$
$ # OR arch -32
$ arch -i386   ./python3 -c 'import sys; print(sys.maxsize == 2**(32 - 1) - 1)'
True
$ # OR arch -64
$ arch -x86_64 ./python3 -c 'import sys; print(sys.maxsize == 2**(64 - 1) - 1)'
True
```

### `pyenv` with official Python

To get the best of both worlds and use the official Python.org binaries
from `pyenv`:

*  [Download][6] the `.pkg` installers for Python 2.7, 3.5, 3.6 and
   any other version you wish to support.
*  Install each of the `.pkg` files (this will require administrator
   privileges, sorry). These will be installed into
   `/Library/Frameworks/Python.framework/Versions/X.Y`.
*  Reset your `${HOME}/.bash_profile`. The Python.org installers will
   have each added a line to your `bash` profile that puts
   `/Library/Frameworks/Python.framework/Versions/X.Y/bin` at
   the beginning of your `${PATH}`. This will "jump in line" in front
   of `pyenv`, which is not what we want.
*  (Optional) Add a `python` executable for the installed Python 3 versions
   (they don't come with `python`, see [PEP 394][9]).

```
$ (cd /Library/Frameworks/Python.framework/Versions/3.5/bin/ && \
>    ln -s python3 python)
$ (cd /Library/Frameworks/Python.framework/Versions/3.6/bin/ && \
>    ln -s python3 python)
```

*  Convince `pyenv` that these are installed versions:

```
$ ln -s /Library/Frameworks/Python.framework/Versions/2.7 \
>   ${HOME}/.pyenv/versions/python-dot-org-2.7
$ ln -s /Library/Frameworks/Python.framework/Versions/3.5 \
>   ${HOME}/.pyenv/versions/python-dot-org-3.5
$ ln -s /Library/Frameworks/Python.framework/Versions/3.6 \
>   ${HOME}/.pyenv/versions/python-dot-org-3.6
```

*  (Optional) Un-confuse `pyenv` about what the **actual** system Python is:

```
$ ln -s /System/Library/Frameworks/Python.framework/Versions/2.7 \
>   ${HOME}/.pyenv/versions/system-2.7
```

*  Execute `pyenv rehash` so the binaries in the new versions get
   registered with `pyenv`.

Once done:

```
$ pyenv versions
  system
* 2.7.14 (set by ${HOME}/.pyenv/version)
* 3.5.4 (set by ${HOME}/.pyenv/version)
* 3.6.2 (set by ${HOME}/.pyenv/version)
* pypy2.7-5.8.0 (set by ${HOME}/.pyenv/version)
  python-dot-org-2.7
  python-dot-org-3.5
  python-dot-org-3.6
  system-2.7
```

[1]: https://github.com/MacPython/wiki/wiki/Spinning-wheels
[2]: http://matthew.dynevor.org
[3]: https://github.com/pyenv/pyenv
[4]: https://brew.sh
[5]: https://pypi.org/project/bezier/0.5.0/
[6]: https://www.python.org/downloads/mac-osx/
[7]: https://conda.io/docs/user-guide/install/macos.html
[8]: https://support.apple.com/en-us/HT204899
[9]: https://www.python.org/dev/peps/pep-0394/
[10]: https://pythonclock.org
[11]: https://en.wikipedia.org/wiki/Universal_binary
[12]: https://docs.python.org/3/library/platform.html#cross-platform
