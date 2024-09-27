# admin_tools/templatetags/sentiment_tags.py

from django import template

register = template.Library()

@register.filter
def sentiment_color(value):
    """
    Returns a CSS class based on the sentiment score.
    - Green for positive (> 60%)
    - Gray for neutral (between -60% and 60%)
    - Red for negative (< -60%)
    """
    try:
        score = int(value)
        if score > 60:
            return 'sentiment-positive'
        elif score < -60:
            return 'sentiment-negative'
        else:
            return 'sentiment-neutral'
    except (ValueError, TypeError):
        return 'sentiment-neutral'

@register.filter
def absolute(value):
    """
    Returns the absolute value of the given number.
    """
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return 0
