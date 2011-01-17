from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from urlr.utils import determine_permalink

from bitly_api import bitly_api


if not getattr(settings, 'BITLY_API_USER', None) or \
   not getattr(settings, 'BITLY_API_KEY', None):
    raise ImproperlyConfigured('Ensure that BITLY_API_USER and BITLY_API_KEY are configured')

bitly = bitly_api.Connection(
    settings.BITLY_API_USER,
    settings.BITLY_API_KEY,
    preferred_domain=getattr(settings, 'BITLY_CUSTOM_DOMAIN', 'bit.ly')
)


class LinkShortenedItemManager(models.Manager):
    def for_object(self, obj):
        return self.get(
            content_type=ContentType.objects.get_for_model(type(obj)),
            object_id=obj.pk
        )

    def get_or_create_for_object(self, obj):
        return self.get_or_create(
            content_type=ContentType.objects.get_for_model(type(obj)),
            object_id=obj.pk
        )

class LinkShortenedItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    shortened_url = models.CharField(max_length=128, blank=True)

    objects = LinkShortenedItemManager()

    def __unicode__(self):
        return self.shortened_url
    
    def save(self, *args, **kwargs):
        if self.content_object and not self.shortened_url:
            try:
                obj_url = self.content_object.get_absolute_url()
                full_url = determine_permalink(Site.objects.get_current(), obj_url)
            except AttributeError:
                pass
            else:
                try:
                    self.shortened_url = bitly.shorten(full_url)['url']
                except bitly_api.BitlyError:
                    pass
        
        super(LinkShortenedItem, self).save(*args, **kwargs)
