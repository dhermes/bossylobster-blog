title: Handling errors in Google App Engine...and failing
date: 2011-11-27
author: Danny Hermes (dhermes@bossylobster.com)
tags: App Engine, Deferred Library, Exception, Google App Engine, Mail API, Metaclass, Python, Pythonic, Request Handler, Task Queue API
slug: handling-errors-in-google-app-engineand
comments: true

After spending a nontrivial amount of my nights and weekends working on
an App Engine app, I wanted a good way to monitor the logs without
checking in on them every day. After a particularly frustrating weekend
of updates that exposed unnoticed bugs that had yet to be triggered by
the app, I set out to find such a way. I set out to find a
[Pythonic](http://docs.python.org/glossary.html#term-pythonic) way.

Since I knew the
[App Engine Mail API](http://code.google.com/appengine/docs/python/mail/) was
super easy to configure, I figured I would just
email myself every time there was an exception, before serving my
default 500 error page. To do so, I just needed to subclass the default
[`RequestHandler`](http://code.google.com/appengine/docs/python/tools/webapp/requesthandlerclass.html)
with my own
[`handle_exception`](http://code.google.com/appengine/docs/python/tools/webapp/requesthandlerclass.html#RequestHandler_handle_exception)
method. (OK, [prepare yourselves](/images/prepare-yourself-for-war.jpg),
a bunch of code is about to happen. See the necessary
[imports](#imports) at the bottom of the post.)

```python
class ExtendedHandler(RequestHandler):

    def handle_exception(self, exception, debug_mode):
        traceback_info = ''.join(format_exception(*sys.exc_info()))
        email_admins(traceback_info, defer_now=True)

        serve_500(self)
```

Awesome! By making all my handlers inherit from `ExtendedHandler`,
I can use the native Python modules `traceback` and `sys`
to get the traceback and my handy dandy

```python
def email_admins(error_msg, defer_now=False):
    if defer_now:
        defer(email_admins, error_msg, defer_now=False)
        return

    sender = 'YOUR APP Errors <errors@your_app_id_here.appspotmail.com>'
    to = 'Robert Admin <bob@example.com>, James Nekbehrd <jim@example.com>'
    subject = 'YOUR APP Error: Admin Notify'
    body = '\n'.join(['Dearest Admin,',
                      '',
                      'An error has occurred in YOUR APP:',
                      error_msg,
                      ''])

    mail.send_mail(sender=sender, to=to,
                   subject=subject, body=body)
```

to send out the email in the
[deferred queue](http://code.google.com/appengine/articles/deferred.html)
as not to hold up the handler serving the page.
Mission accomplished, right? **WRONG!**

Unfortunately, `handle_exception`
[only handles](http://code.google.com/p/googleappengine/issues/detail?id=2110)
the "right" kind of exceptions. That is, exceptions which inherit
directly from Python's ``Exception``.
From the
[horse](/images/your_argument_is_invalid_seahorse.jpg)'s
[mouth](http://docs.python.org/tutorial/errors.html#user-defined-exceptions):

> Exceptions should typically be derived from the
> [`Exception`](http://docs.python.org/library/exceptions.html#exceptions.Exception)
> class, either directly or indirectly.

But. [But](http://www.youtube.com/watch?v=a1Y73sPHKxw)! If the app fails
because a request times out, a `DeadlineExceededError` is thrown and
`handle_exception` falls on its face. Why? Because `DeadlineExceededError`
[inherits](https://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/runtime/__init__.py?r=491#33)
directly from `Exception`'s parent class:`BaseException`.
([Gasp](/images/gasp_by_dokuro-png.jpg))

It's OK little ones, in my
[next post](/2011/11/python-metaclass-for-extra-bad-errors.html)
I explain how I did it while keeping my code Pythonic by using
[metaclasses](http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python#6581949).

## Imports: {#imports}

```python
from google.appengine.api import mail
from google.appengine.ext.deferred import defer
from google.appengine.ext.webapp import RequestHandler
import sysfrom traceback import format_exception
from SOME_APP_SPECIFIC_LIBRARY import serve_500
```

#### Pythonic:

> An idea or piece of code which closely follows the most common idioms
> of the Python language, rather than implementing code using concepts
> common to other languages.

#### Deferred Queue:

Make sure to enable the deferred library in your `app.yaml`
by  using `deferred: on` in your builtins.

<!-- Images not my own but included here for hosting reasons -->
<!-- /images/prepare-yourself-for-war.jpg          -> http://www.troll.me/images/war-cat/prepare-yourself-for-war.jpg -->
<!-- /images/your_argument_is_invalid_seahorse.jpg -> http://gagnamite.com/wp-content/uploads/2013/05/your_argument_is_invalid_seahorse.jpg -->
<!-- /images/gasp_by_dokuro-png.jpg                -> http://vipdictionary.com/img/gasp_by_dokuro-png.jpg -->
