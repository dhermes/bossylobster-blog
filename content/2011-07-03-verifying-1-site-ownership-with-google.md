Title: Verifying 1and1 Site Ownership with Google Apps
date: 2011-07-03
author: Danny Hermes (dhermes@bossylobster.com)
tags: 1and1.com, Django, Google Apps, Verification
slug: verifying-1-site-ownership-with-google

Hello freens. I purchased bossylobster.com from [1&1](http://1and1.com/)
recently with the intent of hosting it on Google App Engine. I soon
found out how delightful this process is. I made a `0.1` version for my
site at [bossylobster.appspot.com](http://bossylobster.appspot.com/) and
decided to launch by clicking **Add Domain** in the **Application Settings**.

<div markdown="1" style="text-align: center;">
  ![Application Settings](/images/verify1and1_screenshot1.png)
</div>

After clicking this I was greeted with a note:

> You must sign up for Google Apps to register this domain or prove that you
> already own it.

Great, so now I had to sign up for Google Apps. (As a side note, at the
time this seemed an unnecessary, annoying wrinkle to add my App, but I
now realize the integration with GMail, Calendar, Docs, etc. is fantastic.)

So here is my ish: prove that you already own it.

Yesterday morning, I spent several hours trying to verify ownership of
bossylobster.com (which I had purchased a week prior). While I realize
the DNS propagation process takes some time, I didn't want to try one
method, wait 24 hours and then realize at that point it hadn't worked.

So, Google Apps
[gives four options](http://www.google.com/support/a/bin/answer.py?answer=60216)
on how to verify:

-   [Create a TXT record](http://www.google.com/support/a/bin/answer.py?answer=183895)
-   Upload an HTML file to a specific path on your site
-   Add a `<meta>` tag to your home page
-   Verify using your Google Analytics tracking code

Well, since I hadn't set my website up, the last three options were off
limits to me (or so I thought). I had a bare minimum package from 1&1,
so hosting was pretty much off limits. Apparently I picked one of the
inept domain hosts because they don't support creation of a CNAME TXT
record!! A quick Google search
[reveals](http://webmasters.stackexchange.com/questions/859/how-can-i-create-an-spf-record-on-my-1and1-com-hosted-domain)

> Yes, we do understand what an SPF record is. Unfortunately we
> do not support in on our hosting plans. We apologize for any
> inconvenience.

<div markdown="1" style="text-align: center;">
  ![Verify Ownership Panel](/images/verify1and1_screenshot2.png)
</div>

So here I am back to square one, just trying to prove I own something,
an inherently basic task made incredibly frustrating. Hopefully I can
help people avoid some frustration with the following instructions.

1.  Open terminal and [change into the directory](http://ss64.com/bash/cd.html)
    with code for bossylobster (your site).
1.  Create a Django project in that directory via the command

        [sudo] django-admin.py startproject bossylobster_django.

    (If you don't have Django or you are using Windows, read these
    [install](https://docs.djangoproject.com/en/1.3/intro/install/)
    instructions, but DON'T SET UP A DATABASE, not necessary here. For a
    more detailed tutorial see
    [this page](https://docs.djangoproject.com/en/1.3/intro/tutorial01/). Also
    note, `startproject` is the function name in the `django-admin` module and
    `bossylobster_django` can be replaced with your project name.
1.  Change the file `bossylobster_django/urls.py` to:

        from django.conf.urls.defaults import patterns
        from django.conf.urls.defaults import url

        urlpatterns = patterns('',
          url(r'^$', 'bossylobster_django.views.index', name='home'),
        )

1.  Change the file `bossylobster_django/views.py` to:

        from django.http import HttpResponse

        def index(request):
          content = '\n'.join([
            '<html>',
            ' <head>',
            '  <meta name="google-site-verification" content="XXXX" />',
            ' </head>',
            ' <body>',
            '  Hello world!',
            ' </body>',
            ' </html>',
          ])
          return HttpResponse(content)

    where `XXXX` should be replaced by the content value provided by Google.

1.  [Determine your internal IP address](http://www.bitwiseim.com/wiki/index.php?title=Determine_your_LAN_/_Local_/_Internal_IP_Address)
    for use in step 6

1.  [Determine your router's (external) IP address](http://checkip.dyndns.com/)
    for use in step 7

1.  Set up a [port forwarding rule](http://portforward.com/dyndns/) in
    your router for port 80 ([websites](https://www.grc.com/port_80.htm))
    with the IP address you found in 4

1.  (After logging in to [1&1](http://1and1.com/))
    [change IP for bossylobster.com](http://faq.1and1.com/domains/domain_admin/dns_settings/13.html)
    to point to your router (from 5)

1.  From the `bossylobster_django` directory (or whatever you called it), run
    the server via

        [sudo] python manage.py runserver 192.168.XX.YY:80

    where `192.168.XX.YY` is the IP you found in 6b.

1.  [Check](http://www.whatsmydns.net/#A/bossylobster.com) to see if
    your change has propagated to DNS servers worldwide (wait until it has)

1.  Upon propagation, login to [Google Apps](https://www.google.com/a)
    and verify via the meta tag

    <div markdown="1" style="text-align: center;">
      ![Verify Ownership Success](/images/verify1and1_screenshot3.png)
    </div>
