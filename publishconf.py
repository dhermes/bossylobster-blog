#!/usr/bin/env python

# This file is used by the `publish` command in the Makefile.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://dhermes.github.io'
DELETE_OUTPUT_DIRECTORY = True
RELATIVE_URLS = True
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
# DISQUS_SITENAME = None
# GOOGLE_ANALYTICS = None
