---
title: A Day in the Life of a (Secure) Request
description: Tracing a request across an ELB and a TLS Reverse Proxy
date: 2020-08-12
author: Danny Hermes (dhermes@bossylobster.com)
tags: TLS, Reverse Proxy, ELB, HTTP
slug: python-list-popleft
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/life-of-a-secure-request.jpg
github_slug: content/2020-08-12-python-list-popleft.md
---

I recently

> It is also possible to use a list as a queue, where the first element added
> is the first element retrieved ("first-in, first-out"); however, lists are
> not efficient for this purpose. While appends and pops from the end of list
> are fast, doing inserts or pops from the beginning of a list is slow (because
> all of the other elements have to be shifted by one).

```c
typedef struct _typeobject {
    PyObject_VAR_HEAD
    // ...
}

typedef ssize_t Py_ssize_t;

#define _PyObject_HEAD_EXTRA

typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
} PyObject;

typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size;
} PyVarObject;

#define PyObject_VAR_HEAD      PyVarObject ob_base;

typedef struct {
    PyObject_VAR_HEAD
    PyObject **ob_item;
    Py_ssize_t allocated;
} PyListObject;
```

Becomes

```python
import ctypes

a = [101, 201, 302, 403, 505, 608, 713]
```

to tear apart a Python `int`

```c
typedef uint32_t digit;

struct _longobject {
    PyObject_VAR_HEAD
    digit ob_digit[1];
};
```

[1]: https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues
[2]: https://github.com/python/cpython/blob/v3.8.2/Doc/tutorial/datastructures.rst
[3]: https://github.com/python/cpython/blob/v3.8.2/Include/listobject.h#L23-L40
[4]: https://github.com/python/cpython/blob/v3.8.2/Include/object.h#L96
[5]: https://github.com/python/cpython/blob/v3.8.2/Include/object.h#L113-L116
[6]: https://github.com/python/cpython/blob/v3.8.2/Include/object.h#L104-L108
[7]: https://github.com/python/cpython/blob/v3.8.2/Include/object.h#L76
[8]: https://github.com/python/cpython/blob/v3.8.2/configure.ac#L5182-L5188
[9]: https://github.com/python/cpython/blob/v3.8.2/Include/cpython/object.h#L177
[10]: https://github.com/python/cpython/blob/v3.8.2/Include/longintrepr.h#L85-L88
[11]: https://github.com/python/cpython/blob/v3.8.2/Include/longintrepr.h#L45
[12]: http://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/
