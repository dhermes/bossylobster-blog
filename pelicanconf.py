# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

import jinja2


CURR_DIR = os.path.abspath(os.path.dirname(__file__))


def get_path(*names):
    return os.path.join(CURR_DIR, *names)


AUTHOR = u"Danny Hermes"

SITENAME = u"Bossy Lobster"
SITESUBTITLE = u"A blog by Danny Hermes; musing on tech, mathematics, etc."
# Default is empty string unless building to publish.
SITEURL = ""
PATH = "content"  # Directory containing posts.

# Times and dates
DEFAULT_DATE_FORMAT = "%b %d, %Y"
TIMEZONE = "US/Pacific"
DEFAULT_LANG = u"en"

# Set the article URL
ARTICLE_URL = "{date:%Y}/{date:%m}/{slug}.html"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{slug}.html"

# Title menu options
ARCHIVES_SAVE_AS = "all-posts.html"
MENUITEMS = [
    ("All Posts", "/{}".format(ARCHIVES_SAVE_AS)),
    ("GitHub", "http://github.com/dhermes/"),
    ("Mathematics", "/mathematics"),
    ("Testimonials", "/testimonials"),
    ("About Me", "/about-me"),
]

# Archive customizations.
NEWEST_FIRST_ARCHIVES = True
HIDE_CATEGORIES_IN_ARCHIVE = True
ARCHIVE_TITLE = "All Posts"

# This assumes pelican>=3.3
STATIC_PATHS = [
    # Folders.
    "css",
    "images",
    "js",
    "latex_images",
    # Files.
    "favicon.ico",
    "favicon.png",
]

# Theme and plugins
THEME = "pelican-octopress-theme/"
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = [
    "summary",
    "simple_footnotes",
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
TWITTER_USER = "bossylobster"
GOOGLE_PLUS_USER = "DannyHermes"
GOOGLE_PLUS_ONE = True
GOOGLE_PLUS_HIDDEN = False
FACEBOOK_LIKE = False
TWITTER_TWEET_BUTTON = True
TWITTER_LATEST_TWEETS = True
TWITTER_FOLLOW_BUTTON = True
TWITTER_TWEET_COUNT = 3
TWITTER_SHOW_REPLIES = "false"
TWITTER_SHOW_FOLLOWER_COUNT = "true"

# Sidebar for the octopress theme, a relative path (to the root).
SIDEBAR_IMAGE = "images/bossy_lobster_350_alpha.png"
SECOND_SIDEBAR_IMAGE = "images/dhermes_headshot.jpg"

# Add extra header.
with open(get_path("extra_header.html"), "r") as file_obj:
    EXTRA_HEADER = file_obj.read()
# NOTE: The liquid_tags.notebook plugin will also create an
#       _nb_header.html file so we should add that if
#       liquid_tags.notebook is to be used.

# Paths to ignore. These are custom files used to render actual
# posts. The `.template` files are Jinja2 templates.
IGNORE_FILES = ["*.template"]

# Adding Disqus comments to page.
DISQUS_SITENAME = "bossylobster"

# Put pages in root. This is strictly for the 404 page.
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# NOTE: This is not secure for actually serving requests, but
#       is fine for static, trusted and known content.
#       See http://stackoverflow.com/a/12340004/1068170.
def escapejs(val):
    return json.dumps(str(val))


JINJA_FILTERS = {"escapejs": escapejs}

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

# If building to publish. This is essentially a `publishconf.py`.
if os.environ.get("PUBLISH") == "true":
    # Required to turn on comments.
    SITEURL = "https://blog.bossylobster.com"
    # Add Google Analytics support.
    GOOGLE_ANALYTICS = "UA-56716324-1"
    # Add Google AdSense.
    with open(get_path("google_adsense_code.html"), "r") as file_obj:
        GOOGLE_ADSENSE_CODE = file_obj.read()

    # RSS/Atom feeds
    FEED_DOMAIN = SITEURL
    FEED_ATOM = "feeds/atom.xml"
    FEED_ALL_ATOM = "feeds/atom.all.xml"
    FEED_RSS = "feeds/rss.xml"
    FEED_ALL_RSS = "feeds/rss.all.xml"

# Search
with open(get_path("custom_search.html"), "r") as file_obj:
    CUSTOM_SEARCH_TEMPLATE = file_obj.read()
CUSTOM_SEARCH = jinja2.Template(CUSTOM_SEARCH_TEMPLATE).render(SITEURL=SITEURL)

# Header
with open(get_path("custom_header.html"), "r") as file_obj:
    CUSTOM_HEADER_TEMPLATE = jinja2.Template(file_obj.read())

# Remove local variables that aren't meant to be used in templates.
del CURR_DIR
del get_path
del file_obj
del CUSTOM_SEARCH_TEMPLATE
