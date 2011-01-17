#!/usr/bin/env python
import sys

from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        BITLY_API_USER='none',
        BITLY_API_KEY='xxx',
        DATABASE_ENGINE='sqlite3',
        ROOT_URLCONF='urlr.tests.urls',
        SITE_ID=1,
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'urlr',
            'urlr.tests',
        ]
    )

from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['urlr']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
