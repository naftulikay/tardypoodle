#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class Config(object):

    def __init__(self, url, headers, keepalive, serial, log_interval=15):
        self.url, self.keepalive, self.serial, self.headers, self.log_interval = \
                url, keepalive, serial, headers, log_interval
