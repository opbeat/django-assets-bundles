import random
import string
import os

INSTALLED_APPS = [
    'django_asset_bundles'
]

SECRET_KEY = ''.join([random.choice(string.ascii_letters) for x in range(40)])

PROJECT_DIR = os.path.dirname(__file__)

ASSETS_MANIFEST_FILE = os.path.join(PROJECT_DIR, 'asset_manifest.json')

ASSETS_URL_BASE = '/static/'
