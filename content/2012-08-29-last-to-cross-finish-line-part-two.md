Title: Last to Cross the Finish Line: Part Two
date: 2012-08-29
author: Danny Hermes (dhermes@bossylobster.com)
tags: AppEngine, Deferred Library, Google App Engine, Google Codesite, Javascript, jQuery, Python, Task Queue API
slug: last-to-cross-finish-line-part-two

Recently, my colleague [+Fred
Sauer](https://plus.google.com/115640166224745944209) and I gave a tech
talk called "Last Across the Finish Line:
Asynchronous [Tasks](https://developers.google.com/appengine/docs/python/taskqueue/overview) with [App
Engine](https://appengine.google.com/)". This is part two in a three
part series where I will share
our [learnings](http://www.forbes.com/pictures/ekij45gdh/learnings/#gallerycontent) and
give some helpful references to the [App Engine
documentation](https://developers.google.com/appengine/docs/).  
  
Check out the [previous
post](http://blog.bossylobster.com/2012/08/last-to-cross-finish-line-part-one.html)
if you haven't already. In this section, we'll cover the two [WSGI
handlers](https://developers.google.com/appengine/docs/python/tools/webapp/running) in
[<span
style="color: lime; font-family: Courier New, Courier, monospace;">main.py</span>](http://code.google.com/p/gae-last-across-the-finish-line/source/browse/main.py)
serving requests for our application and the client side code that
communicates with our application.  

<span style="font-size: large;">Imports</span>
----------------------------------------------

Before defining the handlers, let's first review the imports:  

~~~~ {.prettyprint style="background-color: white;"}
import jsonfrom google.appengine.api import channelfrom google.appengine.api import usersfrom google.appengine.ext.webapp.util import login_requiredimport webapp2from webapp2_extras import jinja2from display import RandomRowColumnOrderingfrom display import SendColorfrom models import PopulateBatch
~~~~

We import [<span
style="color: lime; font-family: Courier New, Courier, monospace;">json</span>](http://docs.python.org/library/json.html)
for serialization of messages. Specific to App Engine, we import <span
style="color: lime; font-family: Courier New, Courier, monospace;">channel</span>
to use the [Channel
API](https://developers.google.com/appengine/docs/python/channel/),
[<span
style="color: lime; font-family: Courier New, Courier, monospace;">users</span>](https://developers.google.com/appengine/docs/python/users/)
and [<span
style="color: lime; font-family: Courier New, Courier, monospace;">login\_required</span>](https://developers.google.com/appengine/docs/python/tools/webapp/utilmodule)
for authenticating users within a request, [<span
style="color: lime; font-family: Courier New, Courier, monospace;">webapp2</span>](https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingwebapp) for
creating [WSGI
Handlers](http://webapp-improved.appspot.com/guide/app.html) and [<span
style="color: lime; font-family: Courier New, Courier, monospace;">jinja2</span>](https://developers.google.com/appengine/docs/python/gettingstartedpython27/templates)
for templating.  
  
Finally, we import four functions from the two other modules defined
within our project. From the [<span
style="color: lime; font-family: Courier New, Courier, monospace;">display</span>](http://code.google.com/p/gae-last-across-the-finish-line/source/browse/display.py)
module, we import the <span
style="color: lime; font-family: Courier New, Courier, monospace;">SendColor</span> function
that we explored in part one and the <span
style="color: lime; font-family: Courier New, Courier, monospace;">RandomRowColumnOrdering</span> function,
which generates all possible row, column pairs in a random order. From
the as of yet undiscussed [<span
style="color: lime; font-family: Courier New, Courier, monospace;">models</span>](http://code.google.com/p/gae-last-across-the-finish-line/source/browse/models.py)
module we import the <span
style="color: lime; font-family: Courier New, Courier, monospace;">PopulateBatch</span>
function, which takes a session ID and a batch of work to be done and
spawns workers to carry out the batch of work.  

<span style="font-size: large;">Handlers</span>
-----------------------------------------------

This module defines two handlers: the main page for the user interface
and an [AJAX](http://en.wikipedia.org/wiki/Ajax_(programming)) handler
which will begin spawning the workers.  
  
For the main page we use <span
style="color: lime; font-family: Courier New, Courier, monospace;">jinja2</span>
templates to render from the template [<span
style="color: lime; font-family: Courier New, Courier, monospace;">main.html</span>](http://code.google.com/p/gae-last-across-the-finish-line/source/browse/templates/main.html)
in the <span
style="color: lime; font-family: Courier New, Courier, monospace;">templates</span>
folder:  

~~~~ {.prettyprint style="background-color: white;"}
class MainPage(webapp2.RequestHandler):  def RenderResponse(self, template, **context):    jinja2_renderer = jinja2.get_jinja2(app=self.app)    rendered_value = jinja2_renderer.render_template(template, **context)    self.response.write(rendered_value)  @login_required  def get(self):    user_id = users.get_current_user().user_id()    token = channel.create_channel(user_id)    self.RenderResponse('main.html', token=token, table_id='pixels',                        rows=8, columns=8)
~~~~

In <span
style="color: lime; font-family: Courier New, Courier, monospace;">get</span>
— the actual handler serving the
[GET](http://en.wikipedia.org/wiki/GET_(HTTP)#Request_methods) request
from the browser — we use the <span
style="color: lime; font-family: Courier New, Courier, monospace;">login\_required</span>
decorator to make sure the user is signed in, and then create a channel
for message passing using the ID of the signed in user. The template
takes an HTML ID, rows and columns to create an HTML table as the
"quilt" that the user will see. We pass the created token for the
channel, an HTML ID for the table and the rows and columns to the
template by simply specifying them as keyword arguments.  
  
For the handler which will spawn the workers, we use <span
style="color: lime; font-family: Courier New, Courier, monospace;">RandomRowColumnOrdering</span>
to generate row, column pairs. Using each pair along with the <span
style="color: lime; font-family: Courier New, Courier, monospace;">SendColor</span>
function and the user ID (as a proxy for session ID) for message
passing, we add a unit of work to the batch  

~~~~ {.prettyprint style="background-color: white;"}
class BeginWork(webapp2.RequestHandler):  # Can't use login_required decorator here because it is not  # supported for POST requests  def post(self):    response = {'batch_populated': False}    try:      # Will raise an AttributeError if no current user      user_id = users.get_current_user().user_id()      # TODO: return 400 if not logged in       work = []      for row, column in RandomRowColumnOrdering(8, 8):        args = (row, column, user_id)        work.append((SendColor, args, {}))  # No keyword args      PopulateBatch(user_id, work)      response['batch_populated'] = True    except:      # TODO: Consider logging traceback.format_exception(*sys.exc_info()) here      pass    self.response.write(json.dumps(response))
~~~~

Finally, for routing applications within our app, we define:  

~~~~ {.prettyprint style="background-color: white;"}
app = webapp2.WSGIApplication([('/begin-work', BeginWork),                               ('/', MainPage)],                              debug=True)
~~~~

and specify   

~~~~ {.prettyprint style="background-color: white;"}
handlers:- url: /.*  script: main.app
~~~~

in <span
style="color: lime; font-family: Courier New, Courier, monospace;">app.yaml</span>;
to use WSGI apps, the App Engine runtime must be <span
style="color: lime; font-family: Courier New, Courier, monospace;">python27</span>.
  

<span style="font-size: large;">Client Side Javascript and jQuery</span>
------------------------------------------------------------------------

In the template [<span
style="color: lime; font-family: Courier New, Courier, monospace;">main.html</span>](http://code.google.com/p/gae-last-across-the-finish-line/source/browse/templates/main.html) we
use [jQuery](http://jquery.com/) to make AJAX requests and manage the
CSS for each square in our "quilt". We also define some other Javascript
functions for interacting with the App Engine Channel API. In the
HTML <span
style="color: lime; font-family: Courier New, Courier, monospace;">\<head\></span> element
we load the [Channel Javascript
API](https://developers.google.com/appengine/docs/python/channel/javascript),
and in the <span
style="color: lime; font-family: Courier New, Courier, monospace;">\<body\></span> element
we open a channel using the <span
style="color: lime; font-family: Courier New, Courier, monospace;">{{
token }}</span> passed in to the template:  

~~~~ {.prettyprint style="background-color: white;"}
<head>  <script src="/_ah/channel/jsapi"></script></head><body>  <script type="text/javascript">    channel = new goog.appengine.Channel('{{ token }}');    socket = channel.open();    socket.onerror = function() { console.log('Socket error'); };    socket.onclose = function() { console.log('Socket closed'); };  </script></body>
~~~~

In addition to <span
style="color: lime; font-family: Courier New, Courier, monospace;">onerror</span>
and <span
style="color: lime; font-family: Courier New, Courier, monospace;">onclose</span>,
we define more complex functions for the <span
style="color: lime; font-family: Courier New, Courier, monospace;">onopen</span>
and <span
style="color: lime; font-family: Courier New, Courier, monospace;">onmessage</span>
callbacks.  
  
First, when the socket has been opened, we send a POST request to <span
style="color: lime; font-family: Courier New, Courier, monospace;">/begin-work</span>
to signal that the channel is ready for communication. If the response
indicates that the batch of workers has been initialized successfully,
we call a method <span
style="color: lime; font-family: Courier New, Courier, monospace;">setStatus</span>
which will reveal the progress spinner:  

~~~~ {.prettyprint style="background-color: white;"}
socket.onopen = function() {  $.post('/begin-work', function(data) {    var response = JSON.parse(data);    if (response.batch_populated) {      setStatus('Loading began');    }  });}
~~~~

As we defined in part one, each <span
style="color: lime; font-family: Courier New, Courier, monospace;">SendColor</span>
worker sends back a
[message](https://developers.google.com/appengine/docs/python/channel/overview#Life_of_a_Typical_Channel_Message)
along the channel representing a row, column pair and a color. On
message receipt, we use these messages to set the background color of
the corresponding square to the color provided:  

~~~~ {.prettyprint style="background-color: white;"}
socket.onmessage = function(msg) {  var response = JSON.parse(msg.data);  var squareIndex = 8*response.row + response.column;  var squareId = '#square' + squareIndex.toString();  $(squareId).css('background-color', response.color);}
~~~~

As you can see from <span
style="color: lime; font-family: Courier New, Courier, monospace;">squareId</span>,
each square in the table generated by the template has an HMTL ID so we
can specifically target it.  

<span style="font-size: large;">Next...</span>
----------------------------------------------

In the [final
post](http://blog.bossylobster.com/2012/09/last-to-cross-finish-line-part-three.html),
we'll define the <span
style="color: lime; font-family: Courier New, Courier, monospace;">PopulateBatch</span>
function and explore the [ndb
models](https://developers.google.com/appengine/docs/python/ndb/) and
[Task
Queue](https://developers.google.com/appengine/docs/python/taskqueue/)
operations that make it work.[About Bossy
Lobster](https://profiles.google.com/114760865724135687241)

</p>

