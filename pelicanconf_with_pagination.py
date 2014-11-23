import sys
# Hack for Travis, where local imports don't work.
if '' not in sys.path:
    sys.path.insert(0, '')

from pelicanconf import *

# Over-ride so there is paging.
DEFAULT_PAGINATION = 5
