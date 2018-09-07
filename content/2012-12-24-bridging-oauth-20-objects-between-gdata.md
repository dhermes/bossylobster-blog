title: Bridging OAuth 2.0 objects between GData and Discovery
date: 2012-12-24
author: Danny Hermes (dhermes@bossylobster.com)
tags: App Engine, Decorator, GData, gdata-python-client, Google App Engine, Google Calendar, google-api-python-client, OAuth, OAuth2.0, Python
slug: bridging-oauth-20-objects-between-gdata
comments: true
github_slug: content/2012-12-24-bridging-oauth-20-objects-between-gdata.md

My colleague
[+Takashi Matsuo](http://plus.google.com/110554344789668969711) and I recently
gave a [talk](http://www.youtube.com/watch?v=HoUdWBzUZ-M) about using
`OAuth2Decorator` (from the `google-api-python-client`
[library](http://code.google.com/p/google-api-python-client/)) with
request handlers in
[Google App Engine](https://developers.google.com/appengine/). Shortly after, a
[Stack Overflow question](http://stackoverflow.com/questions/13981641)
sprung up asking about the right way to use the decorator and, as a
follow up, if the decorator could be used with the
[Google Apps Provisioning API](https://developers.google.com/google-apps/provisioning/).
As I mentioned in my answer,

> The Google Apps Provisioning API is a
> [Google Data API](https://developers.google.com/gdata/docs/2.0/reference) ...
> As a result, you'll need to use the `gdata-python-client`
> [library](http://code.google.com/p/gdata-python-client/) to use the
> Provisioning API. Unfortunately, you'll need to manually convert from a
> [`oauth2client.client.OAuth2Credentials` object](http://code.google.com/p/google-api-python-client/source/browse/oauth2client/client.py?r=efd0ccd31d6c16ddf9f65ba5c31c7033749be0e1#349)
> to a
> [`gdata.gauth.OAuth2Token` object](http://code.google.com/p/gdata-python-client/source/browse/src/gdata/gauth.py?r=cf0208e89433800c713495654774f36d84e894b3#1143)
> to use the same token for either one.

Instead of making everyone and their brother write their own, I thought
I'd take a stab at it and write about it here. The general philosophy I
took was that the token subclass should be 100% based on an
`OAuth2Credentials` object:

- the token constructor simply takes an `OAuth2Credentials` object
- the token refresh updates the `OAuth2Credentials` object set on the token
- values of the current tokencan be updated directly from the
  `OAuth2Credentials` object set on the token

Starting from the top, we'll use two imports:

```python
import httplib2
from gdata.gauth import OAuth2Token
```

The first is needed to refresh an `OAuth2Credentials` object
using the mechanics native to `google-api-python-client`,
and the second is needed so we may subclass the `gdata-python-client` native
token class.

As I mentioned, the values should be updated directly from an
`OAuth2Credentials` object, so in our constructor, we first initialize the
values to `None` and then call our update method to actually set the values.
This allows us to write less code, because,
[repeating is bad](http://en.wikipedia.org/wiki/Don't_repeat_yourself)
(I think someone told me that once?).

```python
class OAuth2TokenFromCredentials(OAuth2Token):
  def __init__(self, credentials):
    self.credentials = credentials
    super(OAuth2TokenFromCredentials, self).__init__(None, None, None, None)
    self.UpdateFromCredentials()
```

We can get away with passing four `None`s to the superclass constructor, as it
only has four positional arguments: `client_id`, `client_secret`, `scope`,
and `user_agent`.

Three of those have equivalents on the `OAuth2Credentials` object, but there
is no place for `scope` because that part of the token exchange is handled
[elsewhere](https://code.google.com/p/google-api-python-client/source/browse/oauth2client/client.py?r=efd0ccd31d6c16ddf9f65ba5c31c7033749be0e1#1030)
in the `google-api-python-client` library.

```python
  def UpdateFromCredentials(self):
    self.client_id = self.credentials.client_id
    self.client_secret = self.credentials.client_secret
    self.user_agent = self.credentials.user_agent
    ...
```

Similarly, the `OAuth2Credentials` object only implements the refresh part of
the OAuth 2.0 flow, so only has the token URI, hence `auth_uri`, `revoke_uri`,
`redirect`, and `_uri` will not be set either. However, the token URI and the
token data are the same for both.

```python
    ...
    self.token_uri = self.credentials.token_uri
    self.access_token = self.credentials.access_token
    self.refresh_token = self.credentials.refresh_token
    ...
```

Finally, we copy the extra fields which may be set outside of a
constructor:

```python
    ...
    self.token_expiry = self.credentials.token_expiry
    self._invalid = self.credentials.invalid
```

Since `OAuth2Credentials` doesn't deal with all parts of the OAuth 2.0
process, we disable those methods from `OAuth2Token` that do.

```python
  def generate_authorize_url(self, *args, **kwargs): raise NotImplementedError
  def get_access_token(self, *args, **kwargs): raise NotImplementedError
  def revoke(self, *args, **kwargs): raise NotImplementedError
  def _extract_tokens(self, *args, **kwargs): raise NotImplementedError
```

Finally, the last method which needs to be implemented is `_refresh`,
which should refresh the `OAuth2Credentials` object and then update the
current GData token after the refresh. Instead of using the passed in request
object, we use one from `httplib2` as we mentioned in imports.

```python
  def _refresh(self, unused_request):
    self.credentials._refresh(httplib2.Http().request)
    self.UpdateFromCredentials()
```

After refreshing the `OAuth2Credentials` object, we can update the current
token using the same method called in the constructor.

Using this class, we can simultaneously call a
[discovery-based API](https://developers.google.com/discovery/v1/getting_started#background)
and a GData API:

```python
from apiclient.discovery import build
from gdata.contacts.client import ContactsClient

service = build('calendar', 'v3', developerKey='...')

class MainHandler(webapp2.RequestHandler):
  @decorator.oauth_required
  def get(self):
    auth_token = OAuth2TokenFromCredentials(decorator.credentials)
    contacts_client = ContactsClient()
    auth_token.authorize(contacts_client)
    contacts = contacts_client.get_contacts()
    ...
    events = service.events().list(calendarId='primary').execute(
        http=decorator.http())
    ...
```
