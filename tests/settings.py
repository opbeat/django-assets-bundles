import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = [
    'tests',
    'django_asset_bundles'
]

# TEST_RUNNER = 'django.test.runner.DiscoverRunner'
STATIC_URL = '/static/'
SECRET_KEY = 'fake-key'
ASSETS_MANIFEST_FILE = os.path.join(BASE_DIR, 'manifests', 'one_dot_zero.json')
ASSETS_URL_BASE = '/static/'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
