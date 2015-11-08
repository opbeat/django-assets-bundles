import json
import os

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.six.moves.urllib.parse import urljoin


VERSION_KEY = 'assets-manifest-version'
DEFAULT_ASSETS_MANIFEST_FILE = os.path.join(
    settings.BASE_DIR,
    'pipeline-manifest.json'
)

_MANIFEST_CACHE = False


class UnknownManifestError(Exception):
    pass


class UnknownAssetError(Exception):
    pass


def handle_1_dot_0(data):
    return data['assets']


def handle_simplified(data):
    return data


supported_versions = {
    '1.0': handle_1_dot_0,
    'simplified': handle_simplified,
}


def static_with_fallback(url):
    if apps.is_installed('django.contrib.staticfiles'):
        return static(url)
    prefix = getattr(settings, 'STATIC_URL', '')
    return urljoin(prefix, url)


def read_manifest(manifest_file_path):
    """
    Determines version of asset manifest file, and returns a mapping of logical
    path to asset path.

    :param manifest_file_path: path to asset manifest file
    :return: dict
    :raises: UnknownManifestError if asset file cannot be read or is in an
             unknown format
    """
    data = None

    if not os.path.exists(manifest_file_path):
        raise UnknownManifestError(
            'No asset manifest file found at {}. Please create it or configure'
            'its location using the ASSETS_MANIFEST_FILE setting'.format(
                manifest_file_path
            )
        )

    with open(manifest_file_path, 'r') as manifest_fd:
        try:
            data = json.loads(manifest_fd.read())
        except ValueError:
            raise UnknownManifestError(
                'The manifest file must be in JSON format'
            )

    if not isinstance(data, dict):
        raise UnknownManifestError('The top level entry must be a dictionary')
    version = data.get(VERSION_KEY)
    if version is None:
        # check if 'assets' key is in data, and its value is a dictionary, in
        # which case we assume 1.0 compatibility
        if 'assets' in data:
            if isinstance(data['assets'], dict):
                version = '1.0'
            else:
                raise UnknownManifestError('"assets" must be a dictionary')
        else:
            # assume simplified version
            version = 'simplified'
    if version in supported_versions:
        return supported_versions[version](data)
    else:
        raise UnknownManifestError(
            'Version {} of the manifest format is not supported'.format(
                version
            )
        )


def get_asset_path(logical_path):
    """
    :param logical_path: logical_path of the asset
    :return: asset path of the asset
    :raises: UnknownAssetError if asset is not defined in manifest
             UnknownManifestError if asset manifest can't be read
    """
    global _MANIFEST_CACHE

    manifest_file_path = getattr(settings, 'ASSETS_MANIFEST_FILE',
                                 DEFAULT_ASSETS_MANIFEST_FILE)

    should_cache = getattr(settings, 'ASSETS_CACHE', not settings.DEBUG)
    if should_cache and _MANIFEST_CACHE:
        assets = _MANIFEST_CACHE
    else:
        assets = read_manifest(manifest_file_path)
        _MANIFEST_CACHE = assets

    try:
        url = assets[logical_path]
    except KeyError:
        raise UnknownAssetError(
            'Logical path "{}" was not found in manifest at {}'.format(
                logical_path,
                manifest_file_path,
            )
        )
    return static_with_fallback(url)
