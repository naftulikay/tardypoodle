#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tardypoodle.data import Config

import argparse

import tardypoodle.concurrent
import tardypoodle.serial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-K', '--disable-keepalive', action='store_false', dest='keepalive',
                        help="Disable keepalive connections.")
    parser.add_argument('-S', '--serial', action='store_true', default=False,
                        help="Execute requests serially without parallelism.")
    parser.add_argument('-H', '--header', action='append', dest='headers', default=[],
                        help="Append a header in curl header format, e.g. 'X-Hello: World'.")
    parser.add_argument('-v', action='count', dest='verbosity', default=0, help="Increase logging verbosity.")
    parser.add_argument('url', help='The URL to test against.')

    args = parser.parse_args()

    # create a dictionary of headers
    headers = {header.split(':')[0]: ':'.join(header.split(':')[1:]).strip() for header in args.headers}

    # initialize logging
    import logging, tardypoodle.utils
    tardypoodle.utils.init_logging(logging.INFO - max(0, args.verbosity * 10))

    # create a config object
    config = Config(url=args.url, headers=headers, keepalive=args.keepalive, serial=args.serial)

    if config.serial:
        tardypoodle.serial.execute(config)
    else:
        tardypoodle.concurrent.execute(config)


if __name__ == "__main__":
    main()
