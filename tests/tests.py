import os

from django.conf import settings
from django.template import Template, Context
from django.test import TestCase
from django.test.utils import override_settings

from django_asset_bundles.readers import (
    read_manifest,
    get_asset_path,
    UnknownAssetError,
    UnknownManifestError)


class AssetTestCase(TestCase):
    def test_get_asset_urls(self):
        test_bundle = get_asset_path('application.js')
        self.assertEqual(test_bundle, '/static/application-6f31.js')

    def test_get_asset_urls_with_staticfiles(self):
        apps = settings.INSTALLED_APPS + ['django.contrib.staticfiles']
        with override_settings(INSTALLED_APPS=apps):
            test_bundle = get_asset_path('application.js')
            self.assertEquals(test_bundle, '/static/application-6f31.js')

    def test_get_asset_urls_not_existing(self):
        self.assertRaises(UnknownAssetError, get_asset_path, 'iamnothere.js')

    def test_templatetag(self):
        template = Template("""
            {% load assets_url %}
            <script src="{% asset "application.js" %}
        """)

        rendered = template.render(Context())
        self.assertIn('/static/application-6f31.js', rendered)


@override_settings(ASSET_CACHE=False)
class ReaderTestCase(TestCase):
    MANIFEST_DIR = os.path.join(os.path.dirname(__file__), 'manifests')

    EXPECTED_ASSETS = {
        "application.css": "application-25b2.css",
        "application.js": "application-6f31.js"
    }

    def get_assets(self, name):
        return read_manifest(os.path.join(self.MANIFEST_DIR, name))

    def test_read_simplified(self):
        assets = self.get_assets('simplified.json')
        self.assertDictEqual(self.EXPECTED_ASSETS, assets)

    def test_one_dot_zero(self):
        assets = self.get_assets('one_dot_zero.json')
        self.assertDictEqual(self.EXPECTED_ASSETS, assets)

    def test_assumed_one_dot_zero(self):
        assets = self.get_assets('assumed_one_dot_zero.json')
        self.assertDictEqual(self.EXPECTED_ASSETS, assets)

    def test_unsupported(self):
        self.assertRaises(
            UnknownManifestError,
            self.get_assets,
            'unsupported.json'
        )

    def test_wrong_assets_type(self):
        self.assertRaises(
            UnknownManifestError,
            self.get_assets,
            'wrong_assets_type.json'
        )

    def test_asset_file_not_existing(self):
        self.assertRaises(
            UnknownManifestError,
            self.get_assets,
            'not_here.json'
        )
