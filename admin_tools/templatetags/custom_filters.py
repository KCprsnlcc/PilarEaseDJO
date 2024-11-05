# admin_tools/templatetags/custom_filters.py

import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Return the base name of the file."""
    return os.path.basename(value)
