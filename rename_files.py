# This is meant to be committed and removed for a one-time
# file rename.

import os
import glob
import json

# In order to pull down all (36) of my blog posts I ran:
# $ pelican-import \
# > --feed http://bossylobster.blogspot.com/feeds/posts/default?max-results=40 \
# > --markup markdown \
# > --output content/


VALID_YEARS = ('2011', '2012', '2013', '2014')
VALID_MONTHS = ['%02d' % val for val in xrange(1, 12 + 1)]


with open('blog_relative_urls.json', 'r') as fh:
    RELATIVE_URLS = json.load(fh)
# This is a relative path, this code assumes it is running
# from the root of this git repository.
EXISTING_POSTS = set(glob.glob('content/*md'))


cleaned_titles = {}
for blog_url in RELATIVE_URLS:
    year, month, title_as_html = blog_url.split('/')
    if year not in VALID_YEARS or month not in VALID_MONTHS:
        raise ValueError(blog_url)
    name, ext = os.path.splitext(title_as_html)
    if ext != '.html':
        raise ValueError(blog_url)
    title_as_md = name + '.md'
    key = (year, month, title_as_md)
    cleaned_titles[key] = os.path.join('content', title_as_md)


if set(cleaned_titles.values()) != EXISTING_POSTS:
    cleaned_only = cleaned_titles - EXISTING_POSTS
    existing_only = EXISTING_POSTS - cleaned_titles
    raise ValueError(('Filenames do not match blog titles',
                      cleaned_only, existing_only))
else:
    print 'Filenames match blog titles.'
