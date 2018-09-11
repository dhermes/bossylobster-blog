---
title: A Python Metaclass for "extra bad" errors in Google App Engine
date: 2011-11-30
author: Danny Hermes (dhermes@bossylobster.com)
tags: App Engine, Class as Object, Decorator, Exception, Google App Engine, Metaclass, OOP, Python, Pythonic, Request Handler
slug: python-metaclass-for-extra-bad-errors
comments: true
github_slug: content/2011-11-30-python-metaclass-for-extra-bad-errors.md
---

So now here we are, having tried to
[handle errors in Google App Engine...and failed](/2011/11/handling-errors-in-google-app-engineand.html)
all because silly `DeadlineExceededError`
[jumps over](https://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/runtime/__init__.py?r=491#33)
`Exception` in the inheritance chain and goes right for `BaseException`.
How can we catch these in our handlers while staying
[Pythonic](http://docs.python.org/glossary.html#term-pythonic)?

First and foremost, in the case of a timeout, we need to explicitly
catch a `DeadlineExceededError`. To do so, we can use a
[decorator](http://stackoverflow.com/questions/739654/understanding-python-decorators#1594484)
(hey, that's Pythonic) in each and every handler for each and every HTTP
verb. (Again,
[prepare yourselves](/images/prepare-yourself.jpg),
a bunch of code is about to happen. See the necessary [imports](#imports)
at the bottom of the post.)

```python
def deadline_decorator(method):

    def wrapped_method(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)
        except DeadlineExceededError:
            traceback_info = ''.join(format_exception(*sys.exc_info()))
            email_admins(traceback_info, defer_now=True)

            serve_500(self)

    return wrapped_method
```

Unfortunately, having to manually decorate
[all the functions](http://knowyourmeme.com/memes/x-all-the-y)
is not so Pythonic. At this point I was stuck and wanted to give up, but
[asked for some advice](https://plus.google.com/u/0/114760865724135687241/posts/GJjXjq5zXhU)
on [G+](http://www.google.com/+) and actually got what I needed from the
all knowing
[Ali Afshar](https://plus.google.com/u/0/118327176775959145936/posts).
What did I need?

> [Metaclasses](http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python#6581949).

Before showing the super simple metaclass I wrote, you need to know one
thing from StackOverflow user
[Kevin Samuel](http://stackoverflow.com/users/9951/kevin-samuel):

> The main purpose of a metaclass is to change the class automatically,
> when it's created.

With the `__new__`
method, the `type`
object in Python actually constructs a class (which is also an object)
by taking into account the name of the class, the parents (or bases) and
the class attritubutes. So, we can make a metaclass by subclassing `type` and overriding
`__new__`:

```python
class DecorateHttpVerbsMetaclass(type):

    def __new__(cls, name, bases, cls_attr):
        verbs = ['get', 'post', 'put', 'delete']
        for verb in verbs:
            if verb in cls_attr and isinstance(cls_attr[verb], function):
                cls_attr[verb] = deadline_decorator(cls_attr[verb])

        return super(DecorateHttpVerbsMetaclass, cls).__new__(cls, name,
                                                              bases, cls_attr)
```

In `DecorateHttpVerbsMetaclass`,
we look for four (of the nine) HTTP
[verbs](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods),
because heck, only seven are supported in
[`RequestHandler`](http://code.google.com/appengine/docs/python/tools/webapp/requesthandlerclass.html),
and we're not that crazy. If the class has one of the verbs as an
attribute **and if** the attribute is a function, we
decorate it with `deadline_decorator`.

Now, we can rewrite our subclass of `RequestHandler`
with one extra line:

```python
class ExtendedHandler(RequestHandler):
    __metaclass__ = DecorateHttpVerbsMetaclass

    def handle_exception(self, exception, debug_mode):
        traceback_info = ''.join(format_exception(*sys.exc_info()))
        email_admins(traceback_info, defer_now=True)

        serve_500(self)
```

By doing this, when the **class** `ExtendedHandler`
is built (as an **object**), all of its attributes and all of its
parent classes (or bases) attributes are checked and possibly updated by
our metaclass.

And now you and James Nekbehrd can feel
[like a boss](http://www.youtube.com/watch?v=NisCkxU544c) when your app
handles errors.

## Imports: {#imports}

```python
from google.appengine.api import mail
from google.appengine.ext.deferred import defer
from google.appengine.ext.webapp import RequestHandler
from google.appengine.runtime import DeadlineExceededError
import sys
from traceback import format_exception
from SOME_APP_SPECIFIC_LIBRARY import serve_500
from LAST_POST import email_admins
```

#### Pythonic:

> An idea or piece of code which closely follows the most common idioms
> of the Python language, rather than implementing code using concepts
> common to other languages.

#### Notes:

-   Using `grep -r "Exception)" . | grep "class "`
    I have convinced myself (for now) that the only errors App Engine will throw
    that do not inherit from `Exception` are `DeadlineExceededError`,
    `SystemExit`, and `KeyboardInterrupt` so that is why I only catch the
    timeout.

-   You can also use `webapp2` to
    [catch 500 errors](http://stackoverflow.com/questions/6853257/how-can-i-setup-a-global-deadlineexceedederror-handler),
    even when `handle_exception` fails to catch them.

#### Disclaimer: <span style="font-weight: normal;">Just because you know what a metaclass is doesn't mean you should use one.</span>

-   *"Don't do stuff like this though, what is your use case?"* - Ali Afshar
-   *"Metaclasses are deeper magic than 99% of users should ever worry
    about. If you wonder whether you need them, you don't (the people
    who actually need them know with certainty that they need them, and
    don't need an explanation about why)."* - Python Guru Tim Peters
-   *"The main use case for a metaclass is creating an API."* -Kevin
    Samuel
