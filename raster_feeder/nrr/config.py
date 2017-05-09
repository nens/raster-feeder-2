# -*- coding: utf-8 -*<F7>-
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from os.path import join
from datetime import timedelta as Timedelta

from ..config import BUILDOUT_DIR  # NOQA
from ..config import STORE_DIR     # NOQA
from ..config import LOG_DIR       # NOQA

# data is read from here
CALIBRATE_DIR = join(BUILDOUT_DIR, 'var', 'calibrate')
CONSISTENT_DIR = join(BUILDOUT_DIR, 'var', 'consistent')

# Default nodatavalue
NODATAVALUE = -9999

# Geographical orientation
GEO_TRANSFORM = -110000, 1000, 0, 700000, 0, -1000
PROJECTION = 'EPSG:28992'

# redis host for mtime cache and turn locking system
REDIS_HOST = 'localhost'
REDIS_DB = 0

# Format for all-digit timestamp
TIMESTAMP_FORMAT = '%Y%m%d%H%M%S'

# Naming of products and files
FRAMESTAMP = dict(f='0005', h='0100', d='2400')
PRODUCT_CODE = {t: {p: 'TF{}_{}'.format(FRAMESTAMP[t], p.upper())
                    for p in 'rnau'}
                for t in 'fhd'}
PRODUCT_TEMPLATE = 'RAD_{code}_{timestamp}.h5'

# Delivery times for various products (not a dict, because order matters)
DELIVERY_TIMES = (
    ('x', Timedelta()),
    ('r', Timedelta()),
    ('n', Timedelta(hours=1)),
    ('a', Timedelta(hours=12)),
    ('u', Timedelta(days=30)),
)

# Import local settings
try:
    from .localconfig import *  # NOQA
except ImportError:
    pass