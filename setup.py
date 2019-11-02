#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name = "tardypoodle",
    version = "0.0.1",
    packages = find_packages('src'),
    package_dir = { '': 'src'},
    author = "Naftuli Kay",
    author_email = "me@naftuli.wtf",
    url = "https://github.com/naftulikay/tardypoodle",
    install_requires = [
        'argparse',
        'gevent == 1.1.1',
        'requests == 2.20.0',
        'setuptools',
        'tzlocal',
    ],
    dependency_links = [],
    entry_points = {
        'console_scripts': [
            'tardypoodle = tardypoodle:main',
        ]
    }
)
