Title: Handling errors in Google App Engine...and failing
date: 2011-11-27
author: Danny Hermes (dhermes@bossylobster.com)
tags: AppEngine, Deferred Library, Exception, Google App Engine, Mail API, Metaclass, Python, Pythonic, Request Handler, Task Queue API
slug: handling-errors-in-google-app-engineand

After spending a nontrivial amount of my nights and weekends working on
an AppEngine app, I wanted a good way to monitor the logs without
checking in on them every day. After a particularly frustrating weekend
of updates that exposed unnoticed bugs that had yet to be triggered by
the app, I set out to find such a way. I set out to find a
[Pythonic\*](http://docs.python.org/glossary.html#term-pythonic)way.

Since I knew the[App Engine Mail
API](http://code.google.com/appengine/docs/python/mail/)was[super
easy](http://t.qkme.me/355773.jpg) to configure, I figured I would just
email myself every time there was an exception, before serving my
default 500 error page. To do so, I just needed to subclass the default
[RequestHandler](http://code.google.com/appengine/docs/python/tools/webapp/requesthandlerclass.html)
with my own [<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">handle\_exception</span>](http://code.google.com/appengine/docs/python/tools/webapp/requesthandlerclass.html#RequestHandler_handle_exception)
method. (OK, [prepare
yourselves](http://troll.me/images/war-cat/prepare-yourself-for-war.jpg),
a bunch of code is about to happen. See the necessary
[imports](http://blog.bossylobster.com/2011/11/handling-errors-in-google-app-engineand.html#imports)
at the bottom of the post.)

~~~~ {.prettyprint style="background-color: white;"}
class ExtendedHandler(RequestHandler):    def handle_exception(self, exception, debug_mode):        traceback_info = ''.join(format_exception(*sys.exc_info()))        email_admins(traceback_info, defer_now=True)        serve_500(self)
~~~~

Awesome! By making all my handlers inherit from <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">ExtendedHandler</span>,
I can use the native Python modules <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">traceback</span>
and <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">sys</span>to
get the traceback and my handy dandy

~~~~ {.prettyprint style="background-color: white;"}
def email_admins(error_msg, defer_now=False):    if defer_now:        defer(email_admins, error_msg, defer_now=False)        return    sender = 'YOUR APP Errors <errors@your_app_id_here.appspotmail.com>'    to = 'Robert Admin <bob@example.com>, James Nekbehrd <jim@example.com>'    subject = 'YOUR APP Error: Admin Notify'    body = '\n'.join(['Dearest Admin,',                      '',                      'An error has occurred in YOUR APP:',                      error_msg,                      ''])    mail.send_mail(sender=sender, to=to,                   subject=subject, body=body)
~~~~

to send out the email in the [deferred
queue\*\*](http://code.google.com/appengine/articles/deferred.html)so
as not to hold up the handler serving the page.[Mission
accomplished](http://www.realdigitalmedia.com/digital-signage-blog/wp-content/uploads/2011/04/Mission-accomplished.jpg),
right? <span class="Apple-style-span"
style="font-size: large;">WRONG!</span>

Unfortunately, <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">handle\_exception</span>
[only
handles](http://code.google.com/p/googleappengine/issues/detail?id=2110)
the "right" kind of exceptions. That is, exceptions which inherit
directly from Python's <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">Exception</span>.
From the
[horse](http://media.comicvine.com/uploads/3/37572/1705127-sea_horse_your_argument_is_invalid_super.jpg)'s
[mouth](http://docs.python.org/tutorial/errors.html#user-defined-exceptions):

> Exceptions should typically be derived from the
> [Exception](http://docs.python.org/library/exceptions.html#exceptions.Exception)
> class, either directly or indirectly.

But. [But](http://www.youtube.com/watch?v=a1Y73sPHKxw)! If the app fails
because a request times out, a<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">DeadlineExceededError</span>is
thrown and <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">handle\_exception</span>
falls on its face. Why? Because<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">DeadlineExceededError</span>[inherits](http://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/runtime/__init__.py#32)directlyfrom<span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">Exception</span>'s
parent class:<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">BaseException</span>.
([Gasp](http://vipdictionary.com/img/gasp_by_dokuro-png.jpg))

It's OK little ones, in my [next
post](http://blog.bossylobster.com/2011/11/python-metaclass-for-extra-bad-errors.html)
I explain how I did it while keeping my code Pythonic by using
[metaclasses](http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python#6581949).

**[Imports:](http://www.blogger.com/blogger.g?blogID=1697307561385480651)**

~~~~ {.prettyprint style="background-color: white;"}
from google.appengine.api import mailfrom google.appengine.ext.deferred import deferfrom google.appengine.ext.webapp import RequestHandlerimport sysfrom traceback import format_exceptionfrom SOME_APP_SPECIFIC_LIBRARY import serve_500
~~~~

**\*Pythonic:**

> *An idea or piece of code which closely follows the most common idioms
> of the Python language, rather than implementing code using concepts
> common to other languages.*

\*\***Deferred Queue**: *Make sure to enable the deferred library in
your*<span class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">app.yaml</span>*by
using*<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">deferred:
on</span>*in your builtins.*

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
