#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import logging
import tzlocal


def init_logging(verbosity=logging.INFO):
    logging.addLevelName(logging.WARNING, "WARN")

    console = logging.StreamHandler()
    console.setFormatter(LoggingFormatter(
        fmt="%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
    ))

    root = logging.getLogger(None)

    root.setLevel(logging.WARNING)
    root.addHandler(console)

    logging.getLogger('tardypoodle').setLevel(verbosity)


class LoggingFormatter(logging.Formatter):
    """A custom logging formatter which supports more date formatting options."""

    DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    TIMEZONE = tzlocal.get_localzone()

    converter = datetime.utcfromtimestamp

    def formatTime(self, record, datefmt=None):
        """Format time using our custom time formatter."""
        if not datefmt:
            datefmt = LoggingFormatter.DEFAULT_DATE_FORMAT

        # by default, no timezone is associated with a datetime, so we create a new one with a timezone
        record_time = LoggingFormatter.TIMEZONE.localize(self.converter(record.created))

        return "".join([
            # iso-8601 slug prefix
            record_time.strftime(datefmt),
            # microsecond to millisecond conversion
            ".{:03.0f}".format(record.msecs),
            # iso-8601 timezone postfix, always UTC due to configuration above
            "Z",
        ])


class RequestCounter(object):

    def __init__(self):
        self.total, self.successful, self.failed, self.http_failures, self.tcp_failures = 0, 0, 0, 0, 0
        self.began, self.ended = None, None

    def __str__(self):
        return "{} Total Requests, {} Successful Requests, {} Failed Requests ({} TCP, {} HTTP)".format(self.total,
                                                                                                        self.successful,
                                                                                                        self.failed,
                                                                                                        self.tcp_failures,
                                                                                                        self.http_failures)

    def start(self):
        self.began = datetime.utcnow()

    def finish(self):
        self.ended = datetime.utcnow()

    def request(self):
        self.total += 1

    def success(self):
        self.successful += 1

    def failed_http(self):
        self.failed, self.http_failures = self.failed + 1, self.http_failures + 1

    def failed_tcp(self):
        self.failed, self.tcp_failures = self.failed + 1, self.tcp_failures + 1

    def duration(self):
        if not self.began and not self.ended:
            return timedelta(0)
        elif self.began and not self.ended:
            return datetime.utcnow() - self.began
        else:
            return self.ended - self.began

    def duration_pretty(self):
        duration = self.duration()

        seconds = duration.seconds
        hours = seconds // 3600
        seconds = seconds - (hours * 3600)
        minutes = seconds // 60
        seconds = seconds - (minutes * 60)

        return "{}h {}m {}s".format(hours, minutes, seconds)
