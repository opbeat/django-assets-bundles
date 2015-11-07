import json
from django.conf import settings
from django import template

_MANIFEST_CACHE = False

class UnknownBundleError(Exception):
    pass

def read_manifest():
    """Returns the manifest. Reads it from settings.ASSETS_MANIFEST_FILE if
    necessary"""
    with open(settings.ASSETS_MANIFEST_FILE, 'r') as manifest_fd:
        return json.loads(manifest_fd.read())


def get_asset_urls(bundle_name):
    """Gets the urls associated with a bundle from the manifest
    @param bundle_name: The bundle name to look for in the manifest
    @rtype : list
    """
    global _MANIFEST_CACHE

    if getattr(settings, 'ASSETS_CACHE', False) and _MANIFEST_CACHE:
        manifest = _MANIFEST_CACHE
    else:
        manifest = read_manifest()
        _MANIFEST_CACHE = manifest

    try:
        urls = manifest[bundle_name]
    except KeyError:
        raise UnknownBundleError("Bundle '{}' was not found in manifest at {}".format(
            bundle_name, settings.ASSETS_MANIFEST_FILE
        ))
    url_base = getattr(settings, 'ASSETS_URL_BASE', '')
    return [url_base + u for u in urls]


register = template.Library()

def do_asset(parser, token):
    tokens = token.split_contents()
    tag_name = tokens[0]
    args = tokens[1:]

    in_quotes = all(
        (n[0] == n[-1] and n[0] in ('"', "'")) for n in args
    )

    if not in_quotes:
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

    # Get rid of quotes
    bundle_names = [n[1:-1] for n in args]

    nodelist = parser.parse(('end_include_bundle',))
    parser.delete_first_token()

    return AssetNode(bundle_names, nodelist)


class AssetNode(template.Node):
    def __init__(self, bundle_names, nodelist):
        self.nodelist = nodelist
        self.bundle_names = bundle_names

    def render(self, context):
        output = ""
        for bundle in self.bundle_names:
            for url in get_asset_urls(bundle):
                context.push()
                context['ASSET_URL'] = url
                output += self.nodelist.render(context)
                context.pop()
        return output

register.tag('include_bundle', do_asset)
