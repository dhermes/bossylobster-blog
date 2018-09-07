title: Last to Cross the Finish Line: Part Three
date: 2012-09-10
author: Danny Hermes (dhermes@bossylobster.com)
tags: App Engine, Deferred Library, Google App Engine, Google Codesite, Javascript, jQuery, Python, Task Queue API
slug: last-to-cross-finish-line-part-three
comments: true
github_slug: content/2012-09-10-last-to-cross-finish-line-part-three.md

Recently, my colleague
[+Fred Sauer](https://plus.google.com/115640166224745944209) and I gave a tech
talk called "Last Across the Finish Line: Asynchronous
[Tasks](https://developers.google.com/appengine/docs/python/taskqueue/overview)
with [App Engine](https://appengine.google.com/)". This is part three in
a three part series where I will share our
[learnings](http://www.forbes.com/pictures/ekij45gdh/learnings/#gallerycontent)
and give some helpful references to the
[App Engine documentation](https://developers.google.com/appengine/docs/).

Check out the
[previous post](/2012/08/last-to-cross-finish-line-part-two.html) if
you haven't already.In this section, we'll define the `PopulateBatch` function
and explore the
[`ndb` models](https://developers.google.com/appengine/docs/python/ndb/)
and
[Task Queue](https://developers.google.com/appengine/docs/python/taskqueue/)
operations that make it work.

Imports
-------

Before defining the
[models](https://developers.google.com/appengine/docs/python/ndb/) and
helper functions in
[`models.py`](http://code.google.com/p/gae-last-across-the-finish-line/source/browse/models.py),
let's first review the imports:

```python
import json

from google.appengine.api import channel
from google.appengine.ext.deferred import defer
from google.appengine.ext import ndb
```

Again, we import [`json`](http://docs.python.org/library/json.html)
and `channel` for serialization and message passing. We import the
`defer` function from the
[deferred library](https://developers.google.com/appengine/articles/deferred) to
abstract away task creation and take advantage of the ability to "defer"
a function call to another thread of execution. Finally, we import `ndb`
as a means for interacting with the App Engine
[Datastore](https://developers.google.com/appengine/docs/python/datastore/overview).

Method Wrapper Built for Tasks
------------------------------

As we saw in the `BeginWork` handler
in [part two](/2012/08/last-to-cross-finish-line-part-two.html),
units of work are passed to `PopulateBatch`
as 3-tuples containing a method, the positional arguments and the
keyword arguments to that method.

In order to keep our task from hanging indefinitely due to unseen errors
and to implicitly include the work unit in the batch, we define a
wrapper around these method calls:

```python
def AlwaysComplete(task, method, *args, **kwargs):
  try:
    method(*args, **kwargs)
  except:  # TODO: Consider failing differently.
    pass
  finally:
    defer(task.Complete)
```

As you can see, we catch any and all errors thrown by our method and
don't retry the method if it fails. In our example, if the call
`method(*args, **kwargs)` fails, the data won't be sent through the channel and
the given square will not show up in the quilt. However, since we catch
these exceptions, the batch will complete and the spinner will disappear
with this square still missing.

This part is likely going to be customized to the specific work
involved, but for our case, we didn't want individual failures to cause
the whole batch to fail. In addition, we implicitly link the work unit
with a special type of task object in the datastore.

In the `finally` section of the error catch, we defer the `Complete`
method on the task corresponding to this work unit. We defer the call to
this complete method in order to avoid any errors (possibly from a
failed datastore action) that the method may cause. If it were to throw
an error, since `AlwaysComplete` is called in a deferred task, the task
would retry and our worker unit would execute (or fail) again, which is bad
if our user interface is not
[idempotent](http://en.wikipedia.org/wiki/Idempotence#Computer_science_meaning).

Task Model
----------

As we saw above, we need a datastore model to represent tasks within a
batch. We start out initially with a model having only one attribute &mdash; a
boolean representing whether or not the task has completed.

```python
class BatchTask(ndb.Model):
  # Very important that the default value True of `indexed` is used here
  # since we need to query on BatchTask.completed
  completed = ndb.BooleanProperty(default=False)
```

As we know, we'll need to define a `Complete` method in order to use the task
in `AlwaysComplete`, but before doing so, we'll define another method which
will put the task object in the datastore and pass a unit of work to
`AlwaysComplete`:

```python
  @ndb.transactional
  def Populate(self, method, *args, **kwargs):
    self.put()
    kwargs['_transactional'] = True
    defer(AlwaysComplete, self.key, method, *args, **kwargs)
```

In this `Populate` method, we first put the object in the datastore
[transactionally](https://developers.google.com/appengine/docs/python/datastore/transactions)
by using the `ndb.transactional` decorator. By adding the `_transactional`
keyword to the keyword arguments, `defer`
[strips away](http://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/ext/deferred/deferred.py?r=277#250)
the underscore and creates a
[transactional task](https://developers.google.com/appengine/docs/python/taskqueue/overview#Tasks_within_Transactions).
By doing this

> the task is only enqueued &mdash; and guaranteed to be enqueued &mdash; if the
> transaction is committed successfully.

We need this deferred task to be enqueued transactionally for consistency of
the `completed` boolean attribute. The datastore put in `Populate` uses the
default value of `False`, but after `Complete` is called we want to set this
boolean to `True`. If this value was not
[consistent](https://developers.google.com/appengine/docs/python/datastore/transactions#Isolation_and_Consistency),
we may have a race condition that resulted in a completed task in the
datastore being marked as incomplete. As we'll see later, we rely on
this consistency for a query that will help us determine if our batch is
done.

To signal that a unit of work has completed, we define the `Complete`
method on the task object:

```python
  @ndb.transactional
  def Complete(self):
    self.completed = True
    self.put()

    batcher_parent = self.key.parent().get()
    defer(batcher_parent.CheckComplete, _transactional=True)
```

It performs two functions. First, it sets `completed` to `True`
in a transaction. Second, it retrieves the parent
[entity](https://developers.google.com/appengine/docs/python/ndb/entities)
of the task object and defers the `CheckComplete` method on this parent.
As we will see in more depth in the `PopulateBatch` function, we use a special
type of batch parent object to create an
[entity group](https://developers.google.com/appengine/docs/python/datastore/entities#Transactions_and_Entity_Groups)
containing all the worker tasks for the batch. We don't want to check if
the batch has completed until the datastore put has succeeded, so we
defer the call to call to `CheckComplete` transactionally, just as we did
with `AlwaysComplete` in the `Populate` method.

> **NOTE**: It may seem that these `get` calls to retrieve the parent via
> `self.key.parent().get()` are using more bandwidth than necessary. However,
> we are relying here on the power of `ndb`. Using a combination of instance
> caching and
> [memcache](https://developers.google.com/appengine/docs/python/memcache/overview),
> most (if not all) of these gets will use the cache and will not incur
> the cost of a round-trip to the datastore.

Batch Parent Model
------------------

Given what we rely on in `BatchTask`, we need to define a special type of
datastore object that will act as the parent entity for a batch. Since we are
going to use it to check when a batch is complete, we define the boolean
attribute `all_tasks_loaded` to signal whether or not all worker tasks from
the batch have begun. We can use this as a short circuit in our `CheckComplete`
method (or as a guard against premature completion).

```python
class TaskBatcher(ndb.Model):
  all_tasks_loaded = ndb.BooleanProperty(default=False, indexed=False)
```

To check if a batch is complete, we first determine if all tasks have
loaded. If that is the case, we perform an
[ancestor query](https://developers.google.com/appengine/docs/python/datastore/queries#Ancestor_Queries)
that simply attempts to fetch the first worker task in the entity group
which has not yet completed. If such a task does not exist, we know the
batch has completed, and so start to clean up the task and batch parent
objects from the datastore.

```python
  def CheckComplete(self):
    # Does not need to be transactional since it doesn't change data
    session_id = self.key.id()
    if self.all_tasks_loaded:
      incomplete = BatchTask.query(BatchTask.completed == False,
                                   ancestor=self.key).fetch(1)
      if len(incomplete) == 0:
        channel.send_message(session_id, json.dumps({'status': 'complete'}))
        self.CleanUp()
        return

    channel.send_message(session_id, json.dumps({'status': 'incomplete'}))
```

We again do the utmost at this step to ensure consistency
by using an ancestor query:

> There are scenarios in which any pending modifications are guaranteed
> to be completely applied ... any ancestor queries in the High
> Replication datastore. In both cases, query results will always be
> current and consistent.

After checking if a batch is complete, we need to communicate the status
back to the client. We'll rely on `PopulateBatch` to create instances of
`TaskBatcher` with the ID of the session corresponding to the batch as the
datastore key. We send a status complete or incomplete message to the client
using the session ID for the channel. In order to correctly handle these
messages on the client, we'll need to update the `onmessage` handler (defined
in [part two](/2012/08/last-to-cross-finish-line-part-two.html))
to account for status updates:

```javascript
socket.onmessage = function(msg) {
  var response = JSON.parse(msg.data);
  if (response.status !== undefined) {
    setStatus(response.status);
  } else {
    var squareIndex = 8*response.row + response.column;
    var squareId = '#square' + squareIndex.toString();
    $(squareId).css('background-color', response.color);
  }}
```

Just as the `setStatus` method revealed the progress spinner when work began,
it will remove the spinner when the status is complete.

We'll next define the `CleanUp` method that is called when the batch is
complete:

```python
  def CleanUp(self):
    children = BatchTask.query(ancestor=self.key).iter(keys_only=True)
    ndb.delete_multi(children)
    self.key.delete()
```

This method uses the key from the batch parent to perform another ancestor
query and creates an object which can
[iterate over all the keys](https://developers.google.com/appengine/docs/python/ndb/queries#iterators)
of the tasks in the batch. By using the `delete_multi` function provided
by `ndb`, we are able to delete these in parallel rather than waiting for each
to complete. After deleting all the tasks, the batcher deletes itself and
clean up is done. Since the `TaskBatcher.CheckComplete` spawns `CleanUp` in
a deferred task, if the deletes time out, the task will try again until
all tasks in the batch are deleted.

As a final method on `TaskBatcher`, we define something similar to
`BatchTask.Populate` that is triggered after all workers in the batch have been
added:

```python
  @ndb.transactional
  def Ready(self):
    self.all_tasks_loaded = True
    self.put()
    self.CheckComplete()
```

This simply signals that all tasks from the batch have loaded by setting
`all_tasks_loaded` to `True` and calls `CheckComplete` in case all the tasks
in the batch have already completed. This check is necessary because if all
worker tasks complete before `all_tasks_loaded` is `True`, then none of the
checks initiated by those tasks would signal completion. We use a transaction
to avoid a race condition with the initial datastore put &mdash; a put which is
a signal that all tasks have **not** loaded.

Populating a Batch
------------------

With our two models in hand, we are finally ready to define the `PopulateBatch`
function used (in
[part two](/2012/08/last-to-cross-finish-line-part-two.html))
by the `BeginWork` handler. We want users of this function to be able to call
it directly, but don't want it to block the process they call it in, so we wrap
the real function in a function that will simply defer the work:

```python
def PopulateBatch(session_id, work):
  defer(_PopulateBatch, session_id, work)
```

In the actual function, we first create a `TaskBatcher` object using the
session ID as the key and put it into the datastore using the default value of
`False` for `all_tasks_loaded`. Since this is a single synchronous `put`, it
blocks the thread of execution and we can be sure our parent is in the datastore
before members of the entity group (the task objects) are created.

```python
def _PopulateBatch(session_id, work):
  batcher_key = ndb.Key(TaskBatcher, session_id)
  batcher = TaskBatcher(key=batcher_key)
  batcher.put()
```

After doing this, we loop through all the 3-tuples in the passed in batch of
`work`. For each unit of work, we create a task using the batcher as parent and
then call the `Populate` method on the task using the method, positional
arguments and keyword arguments provided in the unit of work.

```python
  for method, args, kwargs in work:
    task = BatchTask(parent=batcher_key)
    task.Populate(method, *args, **kwargs)
```

Finally, to signal that all tasks in the batch have been added, we call
the `Ready` method on the batch parent:

```python
  batcher.Ready()
```

> **Note:** This approach can cause performance issues as the number of
> tasks grows, since contentious puts within the entity group can cause
> task completions to stall or retry. I (or my colleagues) will be
> following up with two posts on the following topics:
>
> - using task tagging and pull queues to achieve a similar result, but
>   reducing contention
> - exploring ways to extend this model to a hierarchical model where
>   tasks may have subtasks
