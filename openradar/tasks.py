# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import logging
import os
import sys

import celery

from openradar import config
from openradar import loghelper
from openradar import images
from openradar import scans
from openradar import products
from openradar import publishing
from openradar import utils


# vvv Fix for celery forking problem
os.environ['PYTHONPATH'] = ':'.join(sys.path)

# Autocreate celery db dir
try:
    os.makedirs(os.path.dirname(config.CELERY_DB))
except OSError:
    pass  # No problem.


# Configure celery
app = celery.Celery()
app.conf.update(
    BROKER_URL='sqla+sqlite:///{}'.format(config.CELERY_DB),
)


@celery.task
def do_nothing():
    """ Empty task that can be used as the start of a chain. """


@celery.task
def aggregate(result, datetime, timeframe, radars,
              declutter, direct=False, cascade=False):
    """ Create aggregates and optionally cascade to depending products. """
    loghelper.setup_logging(logfile_name='radar_aggregate.log')
    logging.info(20 * '-' + ' aggregate ' + 20 * '-')
    try:
        # Create aggregates
        aggregate = scans.Aggregate(radars=radars,
                                    declutter=declutter,
                                    datetime=datetime,
                                    timeframe=timeframe)
        aggregate.make()
        # Cascade when requested
        if cascade:
            combinations = utils.get_product_combinations(
                datetimes=[datetime], timeframes=[timeframe],
            )
            for combination in combinations:
                calibrate_kwargs = dict(result=None,
                                        radars=radars,
                                        declutter=declutter,
                                        direct=direct,
                                        cascade=cascade)
                calibrate_kwargs.update(combination)
                if direct:
                    calibrate(**calibrate_kwargs)
                else:
                    calibrate.delay(**calibrate_kwargs)
    except Exception as e:
        logging.exception(e)
    logging.info(20 * '-' + ' aggregate complete ' + 20 * '-')


@celery.task
def calibrate(result, datetime, prodcode, timeframe,
              radars, declutter, direct=False, cascade=False):
    """ Created calibrated aggregated composites. """
    loghelper.setup_logging(logfile_name='radar_calibrate.log')
    logging.info(20 * '-' + ' calibrate ' + 20 * '-')
    try:
        # Create products
        product = products.CalibratedProduct(radars=radars,
                                             prodcode=prodcode,
                                             datetime=datetime,
                                             timeframe=timeframe,
                                             declutter=declutter)
        product.make()
        # Cascade when requested
        if cascade:
            combinations = utils.get_product_combinations(
                datetimes=[datetime],
                prodcodes=[prodcode],
                timeframes=[timeframe],
            )
            for combination in combinations:
                rescale_kwargs = dict(result=None, 
                                      direct=direct,
                                      cascade=cascade)
                rescale_kwargs.update(combination)
                if direct:
                    rescale(**rescale_kwargs)
                else:
                    rescale.delay(**rescale_kwargs)
    except Exception as e:
        logging.exception(e)
    logging.info(20 * '-' + ' calibrate complete ' + 20 * '-')


@celery.task
def rescale(result, datetime, prodcode, timeframe, direct=False, cascade=False):
    """ Create rescaled products wherever possible. """
    loghelper.setup_logging(logfile_name='radar_rescale.log')
    logging.info(20 * '-' + ' rescale ' + 20 * '-')
    try:
        product = products.CalibratedProduct(prodcode=prodcode,
                                             datetime=datetime,
                                             timeframe=timeframe)
        rescaleds = products.Consistifier.create_consistent_products(product)
        if not rescaleds:
            logging.info('Nothing to rescale.')
    except Exception as e:
        logging.exception(e)
    logging.info(20 * '-' + ' rescale complete ' + 20 * '-')


@celery.task
def publish(result, datetimes, prodcodes, timeframes, endpoints, cascade):
    """
    Publish products.

    Cascade means rescaled (derived) products are published as well.
    If the calibrate task is also run with 'cascade=True', this should
    be no problem.
    """
    loghelper.setup_logging(logfile_name='radar_publish.log')
    logging.info(20 * '-' + ' publish ' + 20 * '-')
    try:
        publisher = publishing.Publisher(datetimes=datetimes,
                                         prodcodes=prodcodes,
                                         timeframes=timeframes)
        for endpoint in endpoints:
            getattr(publisher, 'publish_' + endpoint)(cascade=cascade)
    except Exception as e:
        logging.exception(e)
    logging.info(20 * '-' + ' publish complete ' + 20 * '-')


@celery.task
def animate(result, datetime):
    """
    Create animation
    Publish products.

    Cascade means rescaled (derived) products are published as well.
    """
    loghelper.setup_logging(logfile_name='radar_animate.log')
    logging.info(20 * '-' + ' animate ' + 20 * '-')
    try:
        images.create_animated_gif(datetime=datetime)
    except Exception as e:
        logging.exception(e)
    logging.info(20 * '-' + ' animate complete ' + 20 * '-')
