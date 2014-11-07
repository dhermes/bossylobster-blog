# This is meant to be committed and removed for a one-time
# file rename.

import glob
import json
import os


with open('blog_relative_urls.json', 'r') as fh:
    RELATIVE_URLS = sorted(json.load(fh))
EXISTING_POSTS = sorted(glob.glob('content/*md'))


for relative_url, post in zip(RELATIVE_URLS, EXISTING_POSTS):
    if not post.startswith('content/'):
        raise ValueError(post)
    post = post[len('content/'):]

    post_year, post_month, post_title = post.split('-', 2)
    post_title, post_ext = os.path.splitext(post_title)
    if post_ext != '.md':
        raise ValueError(post)

    (rel_url_year, rel_url_month,
     rel_url_title) = relative_url.split('/', 2)
    rel_url_title, rel_url_ext = os.path.splitext(rel_url_title)
    if rel_url_ext != '.html':
        raise ValueError(relative_url)

    if post_year != rel_url_year:
        raise ValueError((relative_url, post))
    if post_month != rel_url_month:
        raise ValueError((relative_url, post))
    if post_title != rel_url_title:
        raise ValueError((relative_url, post))
    print 'Verified %s -> %s' % (relative_url, post)
