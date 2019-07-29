#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tardypoodle.generic import send
from tardypoodle.utils import RequestCounter

import gevent
import gevent.monkey
import logging
import requests.sessions
import sys


def execute(url, headers={}, log_interval=15):
    # keepalive
    session = requests.sessions.session()

    logger = logging.getLogger('tardypoodle.concurrent')
    logger.info("Starting concurrent (gevent) execution of requests...")

    counter = RequestCounter()
    counter.start()

    last_log = log_interval

    gevent.monkey.patch_all()

    try:
        while True:
            gevent.spawn(send, logger=logger, counter=counter, session=session, url=url, headers=headers)

            duration_seconds = counter.duration().seconds

            if duration_seconds % log_interval == 0 and duration_seconds >= last_log:
                logger.info("{}".format(counter))
                last_log = duration_seconds + log_interval
    except KeyboardInterrupt:
        counter.finish()
        logger.info("Shutting down test on terminate signal.")
        logger.info("Test Runtime: {}".format(counter.duration_pretty()))
        logger.info("Results: {}".format(counter))
        sys.exit(0)
