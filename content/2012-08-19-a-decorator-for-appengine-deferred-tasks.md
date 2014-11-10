Title: A Decorator for App Engine Deferred Tasks
date: 2012-08-19
author: Danny Hermes (dhermes@bossylobster.com)
tags: AppEngine, Decorator, Deferred Library, Environment Variables, Google App Engine, Python, Task Queue API
slug: a-decorator-for-appengine-deferred-tasks

I happen to be a big fan of the [deferred
library](https://developers.google.com/appengine/articles/deferred) for
both Python runtimes in [Google App
Engine](https://developers.google.com/appengine/). If an application
needs to queue up work, breaking the work into easy to understand units
by writing worker methods and then deferring the work into tasks is a
breeze using the deferred library. For the majority of cases, if fine
grained control over the method of execution is not needed, using the
deferred library is a great (and in my opinion, the correct)
abstraction.

Maybe I am just biased because I have made a few
[changes](http://blog.bossylobster.com/2012/03/where-have-i-been.html)
to the deferred library over the past few months? One such change I made
added a
[feature](http://code.google.com/p/googleappengine/issues/detail?id=6412)
that allows a task to fail once without having an impact on subsequent
retries; this can be accomplished by raising a <span
style="color: lime; font-family: Courier New, Courier, monospace;">SingularTaskFailure</span>.
Over this weekend, I found that I wanted to use this feature for a
special type\* of worker. Since I wanted to utilize this unique
exception, I wanted to make sure that this worker ***only*** ran in a
deferred task.

Initially I thought I was lost, since any
[pickled](http://docs.python.org/library/pickle.html) method wouldn't
directly have access to the [task queue specific
headers](https://developers.google.com/appengine/docs/python/taskqueue/overview-push#Task_Request_Headers)from
the request. But luckily, many of these headers persist as [environment
variables](http://en.wikipedia.org/wiki/Environment_variable), so can be
accessed via <span
style="color: lime; font-family: Courier New, Courier, monospace;">os.environ</span>
or <span
style="color: lime; font-family: Courier New, Courier, monospace;">os.getenv</span>,
yippee! Being a good little (Python) boy, I decided to abstract this
requirement into a
[decorator](http://stackoverflow.com/questions/739654/understanding-python-decorators#1594484)
and let the function do it's own work in peace.

Upon realizing the usefulness of such a decorator, I decided to write
about it, so here it is:

~~~~ {.prettyprint style="background-color: white;"}
import functoolsimport osfrom google.appengine.ext.deferred import deferfrom google.appengine.ext.deferred.deferred import _DEFAULT_QUEUE as DEFAULT_QUEUEfrom google.appengine.ext.deferred.deferred import _DEFAULT_URL as DEFERRED_URLQUEUE_KEY = 'HTTP_X_APPENGINE_QUEUENAME'URL_KEY = 'PATH_INFO'def DeferredWorkerDecorator(method):  @functools.wraps(method)  def DeferredOnlyMethod(*args, **kwargs):    path_info = os.environ.get(URL_KEY, '')    if path_info != DEFERRED_URL:      raise EnvironmentError('Wrong path of execution: {}'.format(path_info))    queue_name = os.environ.get(QUEUE_KEY, '')    if queue_name != DEFAULT_QUEUE:      raise EnvironmentError('Wrong queue name: {}'.format(queue_name))    return method(*args, **kwargs)  return DeferredOnlyMethod
~~~~

This decorator first checks if the environment variable <span
style="color: lime; font-family: Courier New, Courier, monospace;">PATH\_INFO</span>
is set to the default value for the deferred queue: <span
style="color: lime; font-family: Courier New, Courier, monospace;">/\_ah/queue/deferred</span>.
If this is not the case (or if the environment variable is not set), an
<span
style="color: lime; font-family: Courier New, Courier, monospace;">EnvironmentError</span>
is raised. Then the environment variable <span
style="color: lime; font-family: Courier New, Courier, monospace;">HTTP\_X\_APPENGINE\_QUEUENAME</span>
is checked against the name of the default queue: <span
style="color: lime; font-family: Courier New, Courier, monospace;">default</span>.
Again, if this is incorrect or unset, an <span
style="color: lime; font-family: Courier New, Courier, monospace;">EnvironmentError</span>is
raised. If both these checks pass, the decorated method is called with
its arguments and the value is returned.

To use this decorator:

~~~~ {.prettyprint style="background-color: white;"}
import timefrom google.appengine.ext.deferred import SingularTaskFailure@DeferredWorkerDecoratordef WorkerMethod():  if too_busy():    time.sleep(30)    raise SingularTaskFailure   # do workWorkerMethod()  # This will fail with an EnvironmentErrordefer(WorkerMethod)  # This will perform the work, but in it's own task
~~~~

In case you want to extend this, here is a more "complete" list of some
helpful values that you may be able to retrieve from environment
variables:

~~~~ {.prettyprint style="background-color: white;"}
HTTP_X_APPENGINE_TASKRETRYCOUNTHTTP_X_APPENGINE_QUEUENAMEHTTP_X_APPENGINE_TASKNAMEHTTP_X_APPENGINE_TASKEXECUTIONCOUNTHTTP_X_APPENGINE_TASKETAHTTP_X_APPENGINE_COUNTRYHTTP_X_APPENGINE_CURRENT_NAMESPACEPATH_INFO
~~~~


\***Specialized Worker**:*I had two different reasons to raise a*<span
style="color: lime; font-family: Courier New, Courier, monospace;">SingularTaskFailure</span>*in
my worker. First, I was polling for resources that may not have been
online, so wanted the task to sleep and then restart (after raising the
one time failure). Second, I was using a special sentinel in the
datastore to determine if the current user had any other job in
progress. Again, I wanted to sleep and try again until the current
user's other job had completed.*
