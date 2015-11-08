import warnings

from django import template

from ..readers import get_asset_path

register = template.Library()


@register.simple_tag
def asset(logical_path):
    """
    Usage:
        <script src="{% asset "logical_path" %}"></script>

    :param logical_path:
    :return: an asset path
    """
    asset = get_asset_path(logical_path)
    if not isinstance(asset, basestring):
        warnings.warn("Please use the as_asset filter if your "
                      "pipeline returns lists")
    return asset


@register.filter
def as_asset_list(logical_path):
    """
    Usage:

        {% for file in "logical_path"|as_asset_list %}
            <script src="{{ file }}"></script>
        {% endfor %}

    :param logical_path:
    :return: list of asset paths
    """
    assets = get_asset_path(logical_path)
    if isinstance(assets, basestring):
        return [assets]
    return assets
