#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from tardypoodle.generic import send
from tardypoodle.utils import RequestCounter

import logging
import requests.sessions


def execute(config):
    if config.keepalive:
        requester = requests.sessions.session()
    else:
        requester = requests

    logger = logging.getLogger('tardypoodle.serial')
    logger.info("Starting serial execution of requests...")

    counter = RequestCounter()
    counter.start()

    last_log = config.log_interval

    try:
        while True:
            send(logger=logger, counter=counter, requester=requester, url=config.url, headers=config.headers)

            duration_seconds = counter.duration().seconds

            if duration_seconds % config.log_interval == 0 and duration_seconds >= last_log:
                logger.info("{}".format(counter))
                last_log = duration_seconds + config.log_interval

    except KeyboardInterrupt:
        counter.finish()
        logger.info("Shutting down test on terminate signal.")
        logger.info("Test Runtime: {}".format(counter.duration_pretty()))
        logger.info("Results: {}".format(counter))
