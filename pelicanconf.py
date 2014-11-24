#!/usr/bin/env python

import jinja2
import json
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

# Pagination
DEFAULT_PAGINATION = None

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

# Sidebar for the octopress theme, a relative path (to the root).
SIDEBAR_IMAGE = 'images/bossy_lobster_350_alpha.png'
SECOND_SIDEBAR_IMAGE = 'images/dhermes_headshot.jpg'

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

# Put pages in root. This is strictly for the 404 page.
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# NOTE: This is not secure for actually serving requests, but
#       is fine for static, trusted and known content.
#       See http://stackoverflow.com/a/12340004/1068170.
def escapejs(val):
    return json.dumps(str(val))

JINJA_FILTERS = {'escapejs': escapejs}

# Turn off feeds for translations, author, categories and tags.
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_RSS = None
# Some feed settings can be optionally turned on.
FEED_DOMAIN = None
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
FEED_ATOM = None
FEED_RSS = None

# If building on Travis. This is essentially a `publishconf.py`.
if os.getenv('TRAVIS') == 'true':
    # Required to turn on comments.
    SITEURL = 'https://blog.bossylobster.com'
    # Add Google Analytics support.
    GOOGLE_ANALYTICS = 'UA-56716324-1'
    # Add Google AdSense.
    with open('google_adsense_code.html', 'r') as fh:
        GOOGLE_ADSENSE_CODE = fh.read()

    # RSS/Atom feeds
    FEED_DOMAIN = SITEURL
    FEED_ATOM = 'feeds/atom.xml'
    FEED_ALL_ATOM = 'feeds/atom.all.xml'
    FEED_RSS = 'feeds/rss.xml'
    FEED_ALL_RSS = 'feeds/rss.all.xml'

# Search
with open('custom_search.html', 'r') as fh:
    CUSTOM_SEARCH_TEMPLATE = fh.read()
CUSTOM_SEARCH = jinja2.Template(
    CUSTOM_SEARCH_TEMPLATE).render(SITEURL=SITEURL)
