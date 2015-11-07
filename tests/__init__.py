# -*- coding: utf-8 -*-
import os
import sys
import random
import string

from django.conf import settings


def run_tests():
    from django.test.utils import get_runner
    PROJECT_DIR = os.path.dirname(__file__)
    settings.configure(
        INSTALLED_APPS=[
            'django_asset_bundles'
        ],
        TEST_RUNNER='django.test.runner.DiscoverRunner',
        STATIC_URL='/static/',
        SECRET_KEY=''.join(
            [random.choice(string.ascii_letters) for x in range(40)]),
        ASSETS_MANIFEST_FILE=os.path.join(PROJECT_DIR, 'asset_manifest.json'),
        ASSETS_URL_BASE='/static/',
        DATABASES= {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        }
    )
    import django
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(interactive=False)
    failures = test_runner.run_tests(['django_asset_bundles'])
    return failures


def main():
    failures = run_tests()
    sys.exit(failures)


if __name__ == '__main__':
    main()
