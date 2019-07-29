#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse

import tardypoodle.concurrent
import tardypoodle.serial


def main():
    parser = argparse.ArgumentParser()
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

    if args.serial:
        tardypoodle.serial.execute(args.url, headers)
    else:
        tardypoodle.concurrent.execute(args.url, headers)


if __name__ == "__main__":
    main()
