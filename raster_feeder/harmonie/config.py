# -*- coding: utf-8 -*<F7>-
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
"""
This is the HARMONIE configuration file. It allows for a 'HARMONIE'
localconfig, too, which should be put in the same directory as this module.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from os.path import join

# central config imports
from ..config import BUILDOUT_DIR  # NOQA
from ..config import LOG_DIR       # NOQA

# parameters, names, depths, see http://projects.knmi.nl/
# datacentrum/catalogus/catalogus/content/nl-nwp-harm-grid-p1.htm
PARAMETERS = (
    {
        'group': 'harmonie-inr',   # store group name
        'level': 456,              # rain intensity
        'code': 61,
        'steps': 49,               # available at first step (0 - 48 hr)
    },
    {
        'group': 'harmonie-cr',    # store group name
        'level': 457,              # rain cumulative sum
        'code': 61,
        'steps': 48,               # starts at second step (1 - 48 hr)
    },
    {
        'group': 'harmonie-prcp',  # store group name
        'level': None,             # intensity derived from cumulative sum
        'code': None,
        'steps': 48,               # starts at second step (1 - 48 hr)
    },
    {
        'group': 'harmonie-temp',
        'level': 2,                # air temperature at 2 m in Kelvin
        'code': 11,
        'steps': 49,               # available at first step (0 - 48 hr)
    },
    {
        'group': 'harmonie-rad',
        'level': 0,                # global radiation flux in W / m2
        'code': 117,
        'steps': 48,               # starts at second step (1 - 48 hr)
    },
    {
        'group': 'harmonie-zlto',
        'level': None,             # Referentiegewasverdamping volgens Makkink
        'code': None,
        'steps': 48,
    }
)

# group from which to take the currently stored period
PERIOD_REFERENCE = 'harmonie-inr'  # because it actually starts at step 0

# geographical orientation
GEO_TRANSFORM = -0.0185, 0.037, 0, 55.8885, 0, -0.023
PROJECTION = 'EPSG:4326'

# remote file name strftime() format
FORMAT = 'harm36_v1_ned_surface_%Y%m%d%H.tgz'
PATTERN = 'harm36_v1_ned_surface_[0-9]{10}\.tgz'

# -------------------------------------------
# settings to be overridden in localconfig.py
# -------------------------------------------

# FTP connection
FTP = dict(host='', user='', password='', path='')

# raster store location
STORE_DIR = join(BUILDOUT_DIR, 'var', 'store')

# Lizard RasterStore UUIDs to touch
TOUCH_LIZARD = []

# import local settings
try:
    from .localconfig import *  # NOQA
except ImportError:
    pass
