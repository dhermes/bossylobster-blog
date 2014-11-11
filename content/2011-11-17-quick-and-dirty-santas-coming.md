Title: Quick and Dirty: Santa's Coming
date: 2011-11-17
author: Danny Hermes (dhermes@bossylobster.com)
tags: API, Christmas, GCal, GData, Google Calendar, OAuth, OAuth2.0, Python, Santa
slug: quick-and-dirty-santas-coming

I have been wanting to write a post for awhile, but was travelling for a
[work event](https://sites.google.com/site/barcelonadevfest/) and while
on the road I decided to be lazy.

Since I just so happen to use a few
[GData APIs](http://code.google.com/apis/gdata/) occasionally in my day to day
work, most of the post ideas revolve around quirky things I have done or
want to do with the APIs. Also, due to my obscene love for Python, all
my mashups seem to end up using the
[Python Client for GData](http://code.google.com/p/gdata-python-client/).

#### Back-story:

As I was finalizing travel and gifts for my winter holiday back home, I called
an old friend to let him know I'd be home in 40 days. After relaying this
information to a few other people, I noted to my girlfriend that it would be
nice if a computer would remind me of the count every day. This is where this
quick and dirty pair of scripts come in to remind me when Santa is coming.

#### Pre-work &mdash; Account Settings:

To allow an app to make requests on my behalf, I signed up to
[Manage my Domain](https://accounts.google.com/ManageDomains)
for use with Google Apps, etc. For illustration purposes, let's say I used
`http://example.com` (in reality, I used a pre-existing App of mine, I really
just needed an OAuth token for one time use, no real safety concerns there).
After adding this domain in the management page, I am able to get my
**OAuth Consumer Key** and **OAuth Consumer Secret** which we'll say are
`EXAMPLE_KEY` and `EXAMPLE_SECRET` in this example. Also in the management page,
I set my **OAuth 2.0 Redirect URIs** and made sure my app can serve that page
(even if it is a 404). Again for illustration, let's pretend I used
`http://example.com/verify`.

After doing this settings pre-work, I have two scripts to do the work for me.

## First script &mdash; get the OAuth Token:

```python
import gdata.calendar.client
import gdata.gauth

gcal = gdata.calendar.client.CalendarClient()
oauth_callback = 'http://example.com/verify'
scopes = ['https://www.google.com/calendar/feeds/']
consumer_key = 'EXAMPLE_KEY'
consumer_secret = 'EXAMPLE_SECRET'
request_token = gcal.get_oauth_token(scopes, oauth_callback,
                                     consumer_key, consumer_secret)
out_str = ('Please visit https://www.google.com/accounts/OAuthAuthorize'
           'Token?hd=default&oauth_token=%s' % request_token.token)
print out_str
follow = raw_input('Please entry the follow link after authorizing:\n')
gdata.gauth.authorize_request_token(request_token, follow)
gcal.auth_token = gcal.get_access_token(request_token)
print 'TOKEN:', gcal.auth_token.token
print 'TOKEN_SECRET:', gcal.auth_token.token_secret
```

This script "spoofs" the OAuth handshake by asking the user (me) to go
directly to the
[OAuth Authorize page](https://www.google.com/accounts/OAuthAuthorizeToken).
After doing so and authorizing the App, I am redirected to
`http://example.com/verify` with query parameters for `oauth_verifier`
and `oauth_token`. These are then used by the `gauth`
section of the GData library to finish the OAuth handshake. Once the
handshake is complete, the script prints out a necessary token and token
secret to be used by the second script. I would advise piping the output
to a file, augmenting the script to write them to a file, or writing
these down (this is a joke, please don't write down 40 plus character
goop that was **produced by your computer**). For the next script,
let's pretend our token is `FAKE_TOKEN` and our token secret is
`FAKE_TOKEN_SECRET`.

#### Second script &mdash; insert the events:

```python
# General libraries
from datetime import date
from datetime import timedelta

# Third-party libraries
import atom
import gdata.gauth
import gdata.calendar.client
import gdata.calendar.data

gcal = gdata.calendar.client.CalendarClient()
auth_token = gdata.gauth.OAuthHmacToken(consumer_key='EXAMPLE_KEY',
                                        consumer_secret='EXAMPLE_SECRET',
                                        token='FAKE_TOKEN',
                                        token_secret='FAKE_TOKEN_SECRET',
                                        auth_state=3)
gcal.auth_token = auth_token

today = date.today()
days_left = (date(year=2011, month=12, day=23) - today).days

while days_left >= 0:
    event = gdata.calendar.data.CalendarEventEntry()
    if days_left > 1:
        msg = '%s Days Until Home for Christmas' % days_left
    elif days_left == 1:
        msg = '1 Day Until Home for Christmas'
    elif days_left == 0:
        msg = 'Going Home for Christmas'
    event.title = atom.data.Title(msg)

    # When
    start_time = '2011-%02d-%02dT08:00:00.000-08:00' % (today.month, today.day)
    end_time = '2011-%02d-%02dT09:00:00.000-08:00' % (today.month, today.day)
    event.when.append(gdata.calendar.data.When(
        start=start_time,
        end=end_time,
        reminder=[gdata.data.Reminder(hours='1')]))

    gcal.InsertEvent(event)

    today += timedelta(days=1)
    days_left -= 1
```

This script first authenticates by using the key/secret pair for the
application (retrieved from the settings page) and the key/secret pair
for the user token (that we obtained from the first script). To
authenticate, we explicitly construct an HMAC-SHA1 signed token in the
final auth state (3) of two-legged OAuth and then set the token on our
calendar client (`gcal`).

After authenticating, we start with today and figure out the number of
days in the countdown given my return date of December 23, 2011. With
these in hand, we can loop through until there are no days left,
creating a `CalendarEventEntry` with title as the number of days left
in the countdown and occurring from 8am to 9am PST (UTC -8). Notice also
I include a `gdata.data.Reminder` so I get an email at 7am every morning
(60 minutes before the event) updating my brain on the length of the
countdown!

#### Cleanup:

Be sure to go to your
[issued tokens page](https://accounts.google.com/IssuedAuthSubTokens)
and revoke access to the App (e.g. `http://example.com`)
after doing this to avoid any unwanted security issues.

#### References:

I have never read this, but I'm sure the documentation on
[Registration for Web-Based Applications](http://code.google.com/apis/accounts/docs/RegistrationForWebAppsAuto.html)
is very helpful.

#### Notes:
-   You can annoy other people by inviting them to these events for
    them as well. To do so, simply add the following two lines before
    inserting the event

        who_add = gdata.calendar.data.EventWho(email='name@mail.com')event.who.append(who_add)

-   Sometimes inserting an item results in a RedirectError, so it may
    be safer to try the insert multiple times with a helper function
    such as the following:

        def try_insert(attempts, gcal, event):
            from time import sleep
            from gdata.client import RedirectError

            while attempts > 0:
                try:
                    gcal.InsertEvent(event)
                    break
                except RedirectError:
                    attempts -= 1
                    sleep(3)

            if attempts == 0:
                print 'Insert "%s" failed' % event.title.text

-   In what I swear was a complete coincidence, v3 of the Calendar API was
    [announced](http://googleappsdeveloper.blogspot.com/2011/11/introducing-next-version-of-google.html)
    today. I will try to use the
    [new documentation](https://code.google.com/apis/calendar/v3/getting_started.html)
    to redo this quick and dirty example with v3.
