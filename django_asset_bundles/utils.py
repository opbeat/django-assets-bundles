import json

from django.conf import settings
from django.apps import apps
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.six.moves.urllib.parse import urljoin



_MANIFEST_CACHE = False


class UnknownAssetError(Exception):
    pass


def static_with_fallback(url):
    if apps.is_installed('django.contrib.staticfiles'):
        return static(url)
    prefix = getattr(settings, 'STATIC_URL', '')
    return urljoin(prefix, url)


def read_manifest():
    """Returns the manifest. Reads it from settings.ASSETS_MANIFEST_FILE if
    necessary"""
    with open(settings.ASSETS_MANIFEST_FILE, 'r') as manifest_fd:
        data = json.loads(manifest_fd.read())
    version = data.get('version')
    assets = data['assets']
    return assets


def get_asset_url(logical_path):
    """

    :param label: label of the asset to return
    :return:
    """
    global _MANIFEST_CACHE

    if getattr(settings, 'ASSETS_CACHE', False) and _MANIFEST_CACHE:
        assets = _MANIFEST_CACHE
    else:
        assets = read_manifest()
        _MANIFEST_CACHE = assets

    try:
        url = assets[logical_path]
    except KeyError:
        raise UnknownAssetError("Bundle '{}' was not found in manifest at {}".format(
            logical_path, settings.ASSETS_MANIFEST_FILE
        ))
    return static_with_fallback(url)
