---
title: Silly Pranks on your Friends
date: 2012-04-07
author: Danny Hermes (dhermes@bossylobster.com)
tags: DNS, DNS Lookup, Domain Name System, Hosts file, Internet Protocol, Internet Service Provider, IP Address, ISP, Macbook, nytimes.com, people.com, Practical Joke, Prank, UNIX
slug: silly-pranks-on-your-friends
comments: true
github_slug: content/2012-04-07-silly-pranks-on-your-friends.md
---

## Disclaimer: These are silly little pranks, but I don't encourage messing with someone's computing environment without letting them know you have done so.

### First Prank:

I have a friend who really likes to read
[people.com](http://people.com/), so I figured I would "enrich" her life
a bit with another source of daily news :)

I decided to play around with her
[hosts file](http://en.wikipedia.org/wiki/Hosts_(file)#Purpose), so that when
she visited [people.com](http://people.com/), she really got the
[New York Times](http://nytimes.com/) (the realest news I could think of at
that time, though there are plenty of fine candidates).

To quote the Wikipedia article on `hosts` files:

> The hosts file...assists in addressing network nodes in a computer
> network. It is a common part of an operating system's Internet
> Protocol (IP) implementation, and serves the function of translating
> human-friendly hostnames into numeric protocol addresses, called IP
> addresses, that identify and locate a host in an IP network.

More [importantly][source]:

> the `/etc/hosts` file...allows you to add entries that traditionally
> your computer will look up first before trying your server DNS.

This means that even though the
[DNS Lookup](http://en.wikipedia.org/wiki/Domain_Name_System) provided by her
[ISP](http://en.wikipedia.org/wiki/Internet_service_provider) could
resolve `people.com`, her browser would get an
[IP address](http://en.wikipedia.org/wiki/IP_address) from the hosts file
first and hence will render the New York Times page for
[people.com](http://people.com/).

The first step to do this was to find the IP address for the replacement
site:

```
$ ping www.nytimes.com
PING www.nytimes.com (199.239.136.200): 56 data bytes
64 bytes from 199.239.136.200: icmp_seq=0 ttl=64 time=0.062 ms
64 bytes from 199.239.136.200: icmp_seq=1 ttl=64 time=0.054 ms
...
```

For the second (and final) step, I just needed to add an entry to the
`hosts` file. After
[locating](http://en.wikipedia.org/wiki/Hosts_(file)#Location_in_the_file_system)
the file on her Macbook in `/etc/hosts`, I updated the contents:

```
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1       localhost
255.255.255.255 broadcasthost
::1             localhost
fe80::1%lo0     localhost
199.239.136.200 people.com  # New entry
```

Voil&#0224;! With that, the prank was complete and the next time she visited
[people.com](http://people.com/), the got the contents of
[nytimes.com](http://nytimes.com/) in her browser.

### Second Prank coming soon.

[source]: http://www.justincarmony.com/blog/2011/07/27/mac-os-x-lion-etc-hosts-bugs-and-dns-resolution/
