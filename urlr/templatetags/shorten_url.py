from django import template
from urlr.models import *

register = template.Library()

@register.filter
def shorten(obj):
    """Look for a shortened URL to the object and create one if it does not exist."""
    return LinkShortenedItem.objects.get_or_create_for_object(obj)[0].shortened_url
