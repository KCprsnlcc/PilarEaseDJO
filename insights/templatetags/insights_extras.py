from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary by key
    Usage: {{ my_dict|get_item:my_key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)
