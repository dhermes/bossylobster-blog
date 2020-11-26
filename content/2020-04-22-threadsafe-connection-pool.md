---
title: A Threadsafe Connection Pool for `requests`
description: Using Queue-based Locking for Requests Sessions
date: 2020-04-22
author: Danny Hermes (dhermes@bossylobster.com)
tags: Programming, TCP, Python, Threads
slug: threadsafe-connection-pool
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/requests-python-logo.png
github_slug: content/2020-04-22-threadsafe-connection-pool.md
---

I've been load testing quite a bit recently. So far I've been impressed by the
`wrk` [project's][1] use of sockets to pour on a ridiculously high amount of
load. When I had stretched the system under load **past** its limits, finding
the `fortio` [project][2] was a breath of fresh air, in particular because of
the inclusion of a `-qps` flag to control the rate (and duration) of a load
test.

So what does this have to do with `requests`? These load testing tools (and
many others) are great if you know what to expect of your failures, but I was
load testing to debug a problem. I wanted a way to **keep** all failed
responses and inspect them after the fact; I wanted an **escape hatch** into
the event loop firing off requests.

Motivated by `wrk`, I wanted to utilize a large-ish thread pool all sharing
a connection pool. A shared connection pool enables testing of re-used TCP
sockets and can generate more load since TLS negotiation can be re-used. Using
the `select` [package][4] and low-level [socket][5] objects to accomplish this
task likely would've given maximal throughput but the sheer amount of work
required was not worth it, especially because a modest few hundred requests
per second was all I was looking for (i.e. a controlled but steady flow of
traffic). So I sought to put the &uuml;ber-popular `requests`[ref]Version
`2.23.0`, running Python `3.8.2` on macOS 10.15.4 as of this
writing[/ref]  [package][6] to the task.

### Contents {#contents}

- [Zero Modification Approach](#zero-modification-approach)
- [Zero Correctness](#zero-correctness)
- [Queue and Per-thread Pool](#queue-and-per-thread-pool)
- [Verification](#verification)

### Zero Modification Approach {#zero-modification-approach}

Based on a very popular StackOverflow [question][3], I knew
`requests.Session()` wasn't "really" threadsafe, but I figured I'd give it
a try anyhow. By using a `requests` adapter, a connection pool size can be
specified

```python
import requests


def connection_pool(size):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=size, pool_maxsize=size
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
```

To take it for a test drive, I spun up 4 threads to share a connection pool
of size 2 and at first things looked just fine. Running

```python
import threading


URL = "https://www.google.com/"


def make_request(i, pool):
    response = pool.get(URL)
    print(f"{i} Status Code: {response.status_code}")


def spawn_threads(pool_size, thread_count):
    pool = connection_pool(pool_size)
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(target=make_request, args=(i, pool))
        thread.start()
        threads.append(thread)
    return threads


def main():
    threads = spawn_threads(2, 4)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
```

all 4 threads seem to do their work without interfering with one another

```
1 Status Code: 200
2 Status Code: 200
0 Status Code: 200
3 Status Code: 200
```

### Zero Correctness {#zero-correctness}

To be sure, I added a response hook to actually verify the socket being used
on each request

```python
import socket


def make_response_hook(i):
    def response_hook(response, **unused_kwargs):
        sock = socket.fromfd(
            response.raw.fileno(), socket.AF_INET, socket.SOCK_STREAM
        )
        client_ip, port = sock.getsockname()
        print(f"{i} Socket client address: {client_ip}:{port}")

    return response_hook


def make_request(i, pool):
    response = pool.get(URL, hooks={"response": make_response_hook(i)})
    print(f"{i} Status Code: {response.status_code}")
```

After running this I confirmed that the threads were **not** sharing a pool
of (at most) 2 open TCP sockets:

```
0 Socket client address: 192.168.7.31:50784
0 Status Code: 200
3 Socket client address: 192.168.7.31:50786
3 Status Code: 200
2 Socket client address: 192.168.7.31:50787
1 Socket client address: 192.168.7.31:50785
1 Status Code: 200
2 Status Code: 200
```

To me, this indicates either `requests.Session` directly or some component
(e.g. the underlying `urllib3` [package][8]) is using thread local storage
for parts of the connection pool[ref]I'd love to know more but was more focused
on getting a working multithreaded connection pool.[/ref].
However, using a **global** lock on usage of the connection pool

```python
LOCK = threading.Lock()


def make_request(i, pool):
    with LOCK:
        response = pool.get(URL, hooks={"response": make_response_hook(i)})
    print(f"{i} Status Code: {response.status_code}")
```

it is clear that the **same** socket is used for all requests

```
0 Socket client address: 192.168.7.31:51143
0 Status Code: 200
1 Socket client address: 192.168.7.31:51143
1 Status Code: 200
2 Socket client address: 192.168.7.31:51143
2 Status Code: 200
3 Socket client address: 192.168.7.31:51143
3 Status Code: 200
```

so there is some level of sharing across threads.

### Queue and Per-thread Pool {#queue-and-per-thread-pool}

Since I couldn't directly rely on `requests.Session()` as a multithreaded
pool I sought to create one. I briefly looked into the
`requests_toolbelt.threaded.pool` [module][7] but it also lacks the escape
hatch I was looking for.

Using a **global** lock as above completely defeats the point of concurrent
workers, so this is not an option. Requiring each thread to maintain its own
pool may be unnecessarily restrictive, but due to the state sharing issue each
of the `N` distinct connections will need an exclusive lock.

In order to simulate `N` locks while maintaining some modicum of throughput,
a `queue.Queue()` can be used:

```python
import queue


def threadsafe_pool(size):
    id_queue = queue.Queue(maxsize=size)
    connections = {}
    for i in range(size):
        id_queue.put(i)
        connections[i] = connection_pool(1)
    return connections, id_queue
```

Rather than putting the `requests.Session()` objects directly into the queue,
a read-only dictionary can be shared across all threads. Putting this to use,
the connections and the queue can be passed to the `make_request()` thread
target. The worker can make a (blocking) `get()` for a connection ID from the
queue, keep it until the request has completed and place the connection ID back
on the queue for re-use:

```python
def make_request(i, connections, id_queue):
    connection_id = id_queue.get()
    connection = connections[connection_id]

    response = connection.get(URL, hooks={"response": make_response_hook(i)})

    id_queue.task_done()
    id_queue.put(connection_id)
    print(f"{i} Status Code: {response.status_code}")
```

### Verification {#verification}

To see that this works as expected, the `spawn_threads()` helper can be
updated to pass along the connections and queue

```python
def spawn_threads(pool_size, thread_count):
    connections, id_queue = threadsafe_pool(pool_size)
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(
            target=make_request, args=(i, connections, id_queue)
        )
        thread.start()
        threads.append(thread)
    return threads
```

and running the code shows exactly 2 sockets were used (and re-used)

```
1 Socket client address: 192.168.7.31:51426
1 Status Code: 200
0 Socket client address: 192.168.7.31:51425
0 Status Code: 200
2 Socket client address: 192.168.7.31:51426
2 Status Code: 200
3 Socket client address: 192.168.7.31:51425
3 Status Code: 200
```

Turning up the difficulty level a bit, the sockets used can be tracked
(utilizing the atomicity of `list.append()` in Python)

```python
SOCKET_PAIRS = []


def make_response_hook(i):
    def response_hook(response, **unused_kwargs):
        sock = socket.fromfd(
            response.raw.fileno(), socket.AF_INET, socket.SOCK_STREAM
        )
        SOCKET_PAIRS.append(sock.getsockname())

    return response_hook
```

Using this, a histogram of the sockets

```python
import collections


def main():
    threads = spawn_threads(5, 256)
    for thread in threads:
        thread.join()

    histogram = collections.Counter(SOCKET_PAIRS)
    for (ip_, port), count in histogram.most_common(len(histogram)):
        print(f"{ip_}:{port} -> {count}")
```

shows that only 5 sockets were used to service all 256 requests

```
4 Status Code: 200
0 Status Code: 200
...
255 Status Code: 200
192.168.7.31:51625 -> 52
192.168.7.31:51624 -> 52
192.168.7.31:51621 -> 51
192.168.7.31:51623 -> 51
192.168.7.31:51622 -> 50
```

[1]: https://github.com/wg/wrk
[2]: https://github.com/fortio/fortio
[3]: https://stackoverflow.com/q/18188044/1068170
[4]: https://docs.python.org/3/library/select.html
[5]: https://docs.python.org/3/library/socket.html
[6]: https://requests.readthedocs.io/en/master/
[7]: https://toolbelt.readthedocs.io/en/latest/threading.html
[8]: https://urllib3.readthedocs.io/en/latest/
