import os

PROJECT_DIR = os.path.dirname(__file__)

INSTALLED_APPS = [
    'tests',
    'django_asset_bundles'
]

# TEST_RUNNER = 'django.test.runner.DiscoverRunner'
STATIC_URL = '/static/'
SECRET_KEY = 'fake-key'
ASSETS_MANIFEST_FILE = os.path.join(PROJECT_DIR, 'asset_manifest.json')
ASSETS_URL_BASE = '/static/'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
