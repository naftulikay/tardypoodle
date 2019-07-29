#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import httplib
import requests


def send(logger, counter, requester, url, headers={}):
    logger.debug("Issuing new request...")

    try:
        r = requester.get(url, headers=headers)
    except httplib.HTTPException as e:
        logger.error("Received httplib exception during request: {}".format(e))
        counter.failed_http()
        return
    finally:
        counter.request()

    if not r.status_code == 200:
        logger.warning("HTTP Request Failed: Status {}".format(r.status_code))
        counter.failed_http()
    else:
        logger.debug("Successful request.")
        counter.success()
