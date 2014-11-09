Title: Bridging OAuth 2.0 objects between GData and Discovery
date: 2012-12-24
author: Danny Hermes (dhermes@bossylobster.com)
tags: AppEngine, Decorator, GData, gdata-python-client, Google App Engine, Google Calendar, google-api-python-client, OAuth, OAuth2.0, Python
slug: bridging-oauth-20-objects-between-gdata

My colleague [+Takashi
Matsuo](http://plus.google.com/110554344789668969711)and I recently
gave a [talk](http://www.youtube.com/watch?v=HoUdWBzUZ-M) about using
<span
style="color: lime; font-family: Courier New, Courier, monospace;">OAuth2Decorator</span>
(from the <span
style="color: lime; font-family: Courier New, Courier, monospace;">google-api-python-client</span>
[library](http://code.google.com/p/google-api-python-client/)) with
request handlers in[Google App
Engine](https://developers.google.com/appengine/). Shortly after, a
[Stack Overflow question](http://stackoverflow.com/questions/13981641)
sprung up asking about the right way to use the decorator and, as a
follow up, if the decorator could be used with the [Google Apps
Provisioning
API](https://developers.google.com/google-apps/provisioning/). As I
mentioned in my answer,

> The Google Apps Provisioning API is a [Google Data
> API](https://developers.google.com/gdata/docs/2.0/reference)...As a
> result, you'll need to use the <span
> style="color: lime; font-family: Courier New, Courier, monospace;">gdata-python-client</span>
> [library](http://code.google.com/p/gdata-python-client/) to use the
> Provisioning API. Unfortunately, you'll need to manually convert from
> a [<span
> style="color: lime; font-family: Courier New, Courier, monospace;">oauth2client.client.OAuth2Credentials</span>
> object](http://code.google.com/p/google-api-python-client/source/browse/oauth2client/client.py?r=efd0ccd31d6c16ddf9f65ba5c31c7033749be0e1#349)
> to a [<span
> style="color: lime; font-family: Courier New, Courier, monospace;">gdata.gauth.OAuth2Token</span>
> object](http://code.google.com/p/gdata-python-client/source/browse/src/gdata/gauth.py?r=cf0208e89433800c713495654774f36d84e894b3#1143)
> to use the same token for either one.

Instead of making everyone and their brother write their own, I thought
I'd take a stab at it and write about it here. The general philosophy I
took was that the token subclass should be 100% based on an <span
style="color: lime; font-family: Courier New, Courier, monospace;">OAuth2Credentials</span>
object:

-   the token constructor simply takes an<span
    style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object
-   the token refresh updatesthe<span
    style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object
    set on the token
-   values of the current tokencan be updated directly from the<span
    style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object
    set on the token

Starting from the top, we'll use two imports:

~~~~ {.prettyprint style="background-color: white;"}
import httplib2from gdata.gauth import OAuth2Token
~~~~

The first is needed to refresh an<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object
using the mechanics native to<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">google-api-python-client</span>,
and the second is needed so we may subclass the<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">gdata-python-client</span>native
token class.

As I mentioned, the values should be updated directly from an<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object,
so in our constructor, we first initialize the values to <span
style="color: lime; font-family: Courier New, Courier, monospace;">None</span>
and then call our update method to actual set the values. This allows us
to write less code, because, [repeating is
bad](http://en.wikipedia.org/wiki/Don't_repeat_yourself) (I think
someone told me that once?).

~~~~ {.prettyprint style="background-color: white;"}
class OAuth2TokenFromCredentials(OAuth2Token):  def __init__(self, credentials):    self.credentials = credentials    super(OAuth2TokenFromCredentials, self).__init__(None, None, None, None)    self.UpdateFromCredentials()
~~~~

We can get away with passing four <span
style="color: lime; font-family: Courier New, Courier, monospace;">None</span>s
to the superclass constructor, as it only has four positional arguments:
<span
style="color: lime; font-family: Courier New, Courier, monospace;">client\_id</span>,<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">client\_secret</span>,
<span
style="color: lime; font-family: Courier New, Courier, monospace;">scope</span>,
and <span
style="color: lime; font-family: Courier New, Courier, monospace;">user\_agent</span>.
Three of those have equivalents on the<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object,
but there is no place for<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">scope</span>becausethat
part of the token exchange handled elsewhere (<span
style="color: lime; font-family: Courier New, Courier, monospace;">OAuth2WebServerFlow</span>)in
the<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">google-api-python-client</span>library.

~~~~ {.prettyprint style="background-color: white;"}
  def UpdateFromCredentials(self):    self.client_id = self.credentials.client_id    self.client_secret = self.credentials.client_secret    self.user_agent = self.credentials.user_agent    ...
~~~~

Similarly, the<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object
only implements the refresh part of the OAuth 2.0 flow, so only has the
token URI, hence<span
style="color: lime; font-family: Courier New, Courier, monospace;">auth\_uri</span>,<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">revoke\_uri</span>and<span
style="color: lime; font-family: Courier New, Courier, monospace;">redirect</span><span
style="color: lime; font-family: 'Courier New', Courier, monospace;">\_uri</span>will
not be set either. However, the token URI and the token data are the
same for both.

~~~~ {.prettyprint style="background-color: white;"}
    ...    self.token_uri = self.credentials.token_uri    self.access_token = self.credentials.access_token    self.refresh_token = self.credentials.refresh_token    ...
~~~~

Finally, we copy the extra fields which may be set outside of a
constructor:

~~~~ {.prettyprint style="background-color: white;"}
    ...    self.token_expiry = self.credentials.token_expiry    self._invalid = self.credentials.invalid
~~~~

Since<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>doesn't
deal with all parts of the OAuth 2.0 process, we disable those methods
from<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Token</span>that
do.

~~~~ {.prettyprint style="background-color: white;"}
  def generate_authorize_url(self, *args, **kwargs): raise NotImplementedError  def get_access_token(self, *args, **kwargs): raise NotImplementedError  def revoke(self, *args, **kwargs): raise NotImplementedError  def _extract_tokens(self, *args, **kwargs): raise NotImplementedError
~~~~

Finally, the last method which needs to be implemented is <span
style="color: lime; font-family: Courier New, Courier, monospace;">\_refresh</span>,
which should refresh the<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object
and then update the current GData token after the refresh. Instead of
using the passed in request object, we use one from <span
style="color: lime; font-family: Courier New, Courier, monospace;">httplib2</span>
as we mentioned in imports.

~~~~ {.prettyprint style="background-color: white;"}
  def _refresh(self, unused_request):    self.credentials._refresh(httplib2.Http().request)    self.UpdateFromCredentials()
~~~~

After refreshing the<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">OAuth2Credentials</span>object,
we can update the current token using the same method called in the
constructor.

Using this class, we can simultaneously call a [discovery-based
API](https://developers.google.com/discovery/v1/getting_started#background)
and a GData API:

~~~~ {.prettyprint style="background-color: white;"}
from apiclient.discovery import buildfrom gdata.contacts.client import ContactsClientservice = build('calendar', 'v3', developerKey='...')class MainHandler(webapp2.RequestHandler):  @decorator.oauth_required  def get(self):    auth_token = OAuth2TokenFromCredentials(decorator.credentials)    contacts_client = ContactsClient()    auth_token.authorize(contacts_client)    contacts = contacts_client.get_contacts()    ...    events = service.events().list(calendarId='primary').execute(        http=decorator.http())    ...
~~~~

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
