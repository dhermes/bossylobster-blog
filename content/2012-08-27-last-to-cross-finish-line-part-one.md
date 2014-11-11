Title: Last to Cross the Finish Line: Part One
date: 2012-08-27
author: Danny Hermes (dhermes@bossylobster.com)
tags: App Engine, Deferred Library, Google App Engine, Google Codesite, Javascript, Python, Task Queue API
slug: last-to-cross-finish-line-part-one

Recently, my colleague
[+Fred Sauer](https://plus.google.com/115640166224745944209) and I gave a tech
talk called "Last Across the Finish Line: Asynchronous
[Tasks](https://developers.google.com/appengine/docs/python/taskqueue/overview)
with [App Engine](https://appengine.google.com/)". This is part one in a
three part series where I will share our
[learnings](http://www.forbes.com/pictures/ekij45gdh/learnings/#gallerycontent)
and give some helpful references to the
[App Engine documentation](https://developers.google.com/appengine/docs/).

Intro
-----

Before I dive in, a quick overview of our approach:

-   "Fan out; Fan in" First spread tasks over independent workers; then
    gather the results back together
-   Use task queues to perform background work in parallel
    - Tasks have built-in retries
    - Can respond quickly to the client, making UI more responsive
-   Operate asynchronously when individual tasks can be executed
    independently, hence can be run concurrently
    - If tasks are too work intensive to run synchronously, (attempt
      to) break work into small independent pieces
-   Break work into smaller tasks, for example:
    - rendering media (sounds, images, video)
    - retrieving and parsing data from an external service (Google
      Drive, Cloud Storage, GitHub, ...)
-   Keep track of all workers; notify client when work is complete

Before talking about the sample, let's check it out in action:

<iframe width="560" height="315" src="//www.youtube.com/embed/tEDDVmgN-iU" frameborder="0" allowfullscreen></iframe>

We are randomly generating a color in a worker and sending it back to
the client to fill in a square in the "quilt". (Thanks to
[+Iein Valdez](https://plus.google.com/103073491679741548297) for this term.)
In this example, think of each square as a (most likely more complex)
compute task.

Application Overview
--------------------

The
[application](https://github.com/GoogleCloudPlatform/appengine-last-across-the-finish-line-python)
has a simple structure:

```
gae-last-across-the-finish-line/
|-- app.yaml
|-- display.py
|-- main.py
|-- models.py
+-- templates/
       +-- main.html
```

We'll inspect each of the Python modules `display.py`, `main.py` and `models.py`
individually and explore how they interact with one another. In addition to
this, we'll briefly inspect the HTML and Javascript contained in the template
`main.html`, to understand how the workers pass messages back to the client.

In this post, I will explain the actual background work we did and
briefly touch on the methods for communicating with the client, but
won't get into client side code or the generic code for running the
workers and watching them all as they cross the finish line. In the
second post, we'll examine the client side code and in the third, we'll
discuss the models that orchestrate the work.

Workers
-------

These worker methods are defined in
[`display.py`](http://code.google.com/p/gae-last-across-the-finish-line/source/browse/display.py).
To generate the random colors, we simply choose a hexadecimal digit six
different times and throw a `#` on at the beginning:

```python
import random

HEX_DIGITS = '0123456789ABCDEF'

def RandHexColor(length=6):
  result = [random.choice(HEX_DIGITS) for _ in range(length)]
  return '#' + ''.join(result)
```

With `RandHexColor` in hand, we define a worker that will take a row and column
to be colored and a session ID that will identify the client requesting the
work. This worker will generate a random color and then send it to the
specified client along with the row and column.To pass messages to the
client, we use the
[Channel API](https://developers.google.com/appengine/docs/python/channel/)
and serialize our messages using the
[`json`](http://docs.python.org/library/json.html) library in Python.

```python
import json
from google.appengine.api import channel

def SendColor(row, column, session_id):
  color = RandHexColor(length=6)
  color_dict = {'row': row, 'column': column, 'color': color}
  channel.send_message(session_id, json.dumps(color_dict))
```

Next...
-------

In the
[next post](/2012/08/last-to-cross-finish-line-part-two.html),
we'll explore the
[WSGI handlers](https://developers.google.com/appengine/docs/python/tools/webapp/running)
that run the application and the client side code that handles the
messages from the workers.
