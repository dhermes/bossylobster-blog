#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Danny Hermes'

SITENAME = u'Zoop Zap Title'
SITESUBTITLE = None
SITEURL = ''

PATH = 'content'

# Times and dates
DEFAULT_DATE_FORMAT = '%b %d, %Y'
TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'

# Set the article URL
ARTICLE_URL = None
ARTICLE_SAVE_AS = None

# Title menu options
MENUITEMS = [('Archives', '/archives.html'),
             ('Home Page', 'XX')]
NEWEST_FIRST_ARCHIVES = False

# Theme and plugins
THEME = 'pelican-octopress-theme/'
PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['summary', 'liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook',
           'liquid_tags.literal']

DISPLAY_PAGES_ON_MENU = False

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
