from django.template import Template, Context
from django_asset_bundles.templatetags.assets_url import get_asset_urls, \
    UnknownBundleError

import pytest


def test_get_asset_urls():
    test_bundle = get_asset_urls('lib_js')

    assert test_bundle == ['/static/build/libs.min.js']


def test_get_asset_urls_not_existing():

    with pytest.raises(UnknownBundleError):
        test_bundle = get_asset_urls('non_existent_bundle')


def test_templatetag():
    template = Template("""
        {% load assets_url %}
        {% include_bundle "lib_js" %}
        <script type="text/javascript" src="{{ ASSET_URL }}" charset="utf-8"></script>
        {% end_include_bundle %}
    """)

    rendered = template.render(Context())

    assert '/static/build/libs.min.js' in rendered


