from django.utils.html import format_html
from django import template

register = template.Library()


@register.filter
def org_desc(val):
    if isinstance(val, str):
        if len(val) >= 20:
            val = val[:20] + '...'
        else:
            val = val[:20]
    return val



