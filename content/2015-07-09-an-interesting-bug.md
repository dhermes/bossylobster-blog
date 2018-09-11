---
title: An Interesting Bug
description: Buggy Interview Question; Set for Life
date: 2015-07-09
author: Danny Hermes (dhermes@bossylobster.com)
tags: Debugging, Programming, Python, Interview
slug: an-interesting-bug
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
github_slug: content/2015-07-09-an-interesting-bug.md
---

A fairly [common][1] interview [question][2] is

> What is the "hardest" bug you've dealt with?

I've both asked it and answered it in interviews. It's pretty rare
that the answer is useful and actionable, but I'll hold off on
commenting on the state of the art in tech interviews today.
(Usually the interviewer defines what "hardest" means or the
interviewee asks for more specifics.)

Though it's been a few years since I've interviewed for jobs, I
still can recall the discomfort at not having a good answer for
this question. (Probably exacerbated by the fact that I was
asking candidates a question I didn't have a good answer to.)

However, I recently acquired a good answer. Immediately after tracking
down a "bug" in the `oauth2client` library, I realized that I was
set for (interview) life.

### First Contact

A user reported a [bug][3] in a library I maintain. The evidence of the
bug was an obscure HTTP response (`{'error': 'invalid_grant'}`) rather
than an errant code path.

My initial instinct was that for some reason, the user was sending a
malformed request due to encoding issues. This library notoriously
has had many bugs involving the support for Python 2 and 3
simultaneously and these often lead to incorrect representation of
text (mixing up `bytes` and unicode).

### Debugging

After some futile back-and-forth on the bug report, it was clear
that I'd need to be on the failing machine to really determine
what was happening. (This was made clear by the fact that the user
could successfully execute the same code on OS X that failed on
an EC2 instance ... **foreshadowing**.)

I hopped onto a screenshare with the user and we went to work.
The first thing we did was to step into the failing [line][4]
of code. We ran the failing script with `ipython -i`
(interactive mode) and then used the [`%debug` magic][5] to
step into the code right where the exception occurred.

On checking the [JSON web token (JWT)][6] in the `body`,
it was clear that the header, payload and signed final
segment were correct on both OS X and his EC2 instance.

### Check the Crypto

Since the plaintext (base64 encoded JSON) header and payload
segments of the JWT were valid, we next stepped into
the [`make_signed_jwt` function][7] to ensure that the
JWT signature was being created correctly on both machines.

We even copied and pasted identical header and payload strings
and found **identical** signatures on OS X and the EC2
instance (running Ubuntu).

### Not Crypto, Not Cryptic

At this point, I was completely perplexed. The request was
seemingly perfectly constructed and &mdash; given the same
inputs &mdash; both operating systems performed identically.

But the [user][8] that filed the bug had the key insight. The
assumption **"given the same inputs"** was now the point of
failure.

He looked at the payload

```json
{
  "aud": "https://accounts.google.com/o/oauth2/token",
  "exp": 1433902178,
  "iat": 1433898578,
  "iss": "1234567890-random-id@developer.gserviceaccount.com",
  "scope": "https://www.googleapis.com/auth/userinfo.email"
}
```

and realized the timestamps (`exp` for expired and `iat` for
issued at, which are an hour, i.e. 3600 seconds apart) were
drastically different from OS X to the EC2 instance!

These are determined as seconds since the [epoch][9]:

```python
>>> import datetime
>>> int(time.mktime(datetime.datetime.utcnow().timetuple()))
1433898578
```

### Final Solution

After this realization, the answer was quite simple:

> The clock had drifted on the EC2 instance and the time was
> wrong. In fact, it was 450 minutes in the past.

So when the `oauth2client` library issued requests, it asked
for tokens that expired 390 minutes in the past (an hour past
the "current" time on the machine). Complying with this is
an impossibility, hence the invalid grant error.

This most interesting bug wasn't a bug in the library, but an
incorrectly configured local environment. Once we realized
this fact, the fix was as simple as:

```bash
$ sudo ntpdate -s ntp.ubuntu.com
```

[1]: http://stackoverflow.com/q/169713/1068170
[2]: http://www.quora.com/Whats-the-hardest-bug-youve-debugged
[3]: https://github.com/google/oauth2client/issues/193
[4]: https://github.com/google/oauth2client/blob/fe246ba9bf9044c4f81826825b72e86489bae72d/oauth2client/client.py#L833
[5]: https://ipython.org/ipython-doc/dev/interactive/magics.html#magic-debug
[6]: http://jwt.io/
[7]: https://github.com/google/oauth2client/blob/fe246ba9bf9044c4f81826825b72e86489bae72d/oauth2client/crypt.py#L384
[8]: https://twitter.com/michalmigurski
[9]: https://en.wikipedia.org/wiki/Unix_time
