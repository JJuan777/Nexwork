import base64
from django import template

register = template.Library()

@register.filter
def to_base64(value):
    if value:
        return "data:image/png;base64," + base64.b64encode(value).decode()
    return ""
