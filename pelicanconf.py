#!/usr/bin/env python

import os


AUTHOR = u'Danny Hermes'

SITENAME = u'Bossylobster Blog'
SITESUBTITLE = (u'Musings on humor/tech/mathematics/sports '
                'from the bossiest lobster')
# Default is empty string unless building on Travis.
SITEURL = ''
PATH = 'content'  # Directory containing posts.

# Times and dates
DEFAULT_DATE_FORMAT = '%b %d, %Y'
TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'

# Set the article URL
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'

# Title menu options
ARCHIVES_SAVE_AS = 'all_posts.html'
MENUITEMS = [
    ('All Posts', '/%s' % ARCHIVES_SAVE_AS),
    ('GitHub Profile', 'http://github.com/dhermes/'),
    ('Berkeley Page', 'http://math.berkeley.edu/~dhermes/'),
]

# Archive customizations.
NEWEST_FIRST_ARCHIVES = True
HIDE_CATEGORIES_IN_ARCHIVE = True
ARCHIVE_TITLE = 'All Posts'

# This assumes pelican>=3.3
STATIC_PATHS = [
    # Folders.
    'css',
    'images',
    'js',
    'latex_images',
    # Files.
    'favicon.ico',
    'favicon.png',
]

# Theme and plugins
THEME = 'pelican-octopress-theme/'
PLUGIN_PATHS = [
    'pelican-plugins',
]
PLUGINS = [
    'summary',
    # These tags currently fail when building with Pelican 3.5.
    # 'liquid_tags.include_code',
    # 'liquid_tags.notebook',
]

# Some menu settings
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
HIDE_TAGS_IN_SIDEBAR = True
HIDE_CATEGORIES_IN_SIDEBAR = True

# Sharing
TWITTER_USER = 'bossylobster'
GOOGLE_PLUS_USER = 'DannyHermes'
GOOGLE_PLUS_ONE = True
GOOGLE_PLUS_HIDDEN = False
FACEBOOK_LIKE = False
TWITTER_TWEET_BUTTON = True
TWITTER_LATEST_TWEETS = True
TWITTER_FOLLOW_BUTTON = True
TWITTER_TWEET_COUNT = 3
TWITTER_SHOW_REPLIES = 'false'
TWITTER_SHOW_FOLLOWER_COUNT = 'true'

# RSS/Atom feeds intentionally not used. Will revisit.
# See ('http://docs.getpelican.com/en/latest/faq.html'
#      '#what-if-i-want-to-disable-feed-generation')
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Search
SEARCH_BOX = True

# Sidebar for the octopress theme, a relative path (to the root).
SIDEBAR_IMAGE = 'images/bossy_lobster_200_alpha.png'

# Add extra header.
EXTRA_HEADER = open('extra_header.html').read().decode('utf-8')
# NOTE: The liquid_tags.notebook plugin will also create an
#       _nb_header.html file so we should add that if
#       liquid_tags.notebook is to be used.

# Paths to ignore. These are custom files used to render actual
# posts. The `.template` files are Jinja2 templates.
IGNORE_FILES = ['*.template']

# Adding Disqus comments to page.
DISQUS_SITENAME = 'bossylobster'

# Put pages in root. This is primarily for the 404 page.
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# If building on Travis. This is essentially a `publishconf.py`.
if os.getenv('TRAVIS') == 'true':
    # Required to turn on comments.
    SITEURL = 'https://dhermes.github.io'

GOOGLE_ADSENSE_CODE = """\
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- responsive-blog-ad -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-4173900012268590"
     data-ad-slot="9363500864"
     data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""
