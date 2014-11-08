#!/usr/bin/env python

AUTHOR = u'Danny Hermes'

SITENAME = u'Bossylobster Blog'
SITESUBTITLE = (u'Musings on humor/tech/mathematics/sports '
                'from the bossiest lobster')
SITEURL = ''  # This is changed in publishconf.py.
PATH = 'content'  # Directory containing posts.

# Times and dates
DEFAULT_DATE_FORMAT = '%b %d, %Y'
TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'

# Set the article URL
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'

# Title menu options
MENUITEMS = [
    ('All Posts', '/archives.html'),
    ('GitHub Profile', 'http://github.com/dhermes/'),
    ('Berkeley Page', 'http://math.berkeley.edu/~dhermes/'),
]

# Archive customizations.
NEWEST_FIRST_ARCHIVES = True
HIDE_CATEGORIES_IN_ARCHIVE = True
ARCHIVE_TITLE = 'All Posts'

# This assumes pelican>=3.3
STATIC_PATHS = [
    'images',
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

# RSS/Atom feeds intentionally not used.
# FEED_DOMAIN = None
# FEED_ATOM = None

# Search
SEARCH_BOX = True

# Sidebar for the octopress theme, a relative path (to the root).
SIDEBAR_IMAGE = 'images/bossy_lobster_200_alpha.png'
