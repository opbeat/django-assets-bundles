from django.conf import settings
from django.template import Template, Context
from django.test import TestCase
from django.test.utils import override_settings

from django_asset_bundles.utils import (
    get_asset_url,
    UnknownAssetError,
)


class AssetTestCase(TestCase):
    def test_get_asset_urls(self):
        test_bundle = get_asset_url('application.js')
        self.assertEqual(test_bundle, '/static/application-6f31.js')

    def test_get_asset_urls_with_staticfiles(self):
        apps = settings.INSTALLED_APPS + ['django.contrib.staticfiles']
        with override_settings(INSTALLED_APPS=apps):
            test_bundle = get_asset_url('application.js')
            self.assertEquals(test_bundle, '/static/application-6f31.js')

    def test_get_asset_urls_not_existing(self):
        self.assertRaises(UnknownAssetError, get_asset_url, 'iamnothere.js')

    def test_templatetag(self):
        template = Template("""
            {% load assets_url %}
            <script src="{% asset "application.js" %}
        """)

        rendered = template.render(Context())
        self.assertIn('/static/application-6f31.js', rendered)


