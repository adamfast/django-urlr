from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from bitly_api import bitly_api

class LinkShortenedItemManager(models.Manager):
    def for_object(self, obj):
        return self.get(content_type=ContentType.objects.get_for_model(obj.__class__), object_id=obj.pk)

class LinkShortenedItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    shortened_url = models.CharField(max_length=128, blank=True)

    objects = LinkShortenedItemManager()

    def __unicode__(self):
        return self.shortened_url

def shorten_link(sender, **kwargs):
    """Run when a LinkShortenedItem is saved and ensure that a shortened link is available."""
    lsi = kwargs['instance']
    if not lsi.shortened_url:
        if not getattr(settings, 'BITLY_API_USER', False):
            raise ImproperlyConfigured
        if not getattr(settings, 'BITLY_API_KEY', False):
            raise ImproperlyConfigured
        c = bitly_api.Connection(settings.BITLY_API_USER, settings.BITLY_API_KEY, preferred_domain=getattr(settings, 'BITLY_CUSTOM_DOMAIN', 'bit.ly'))
        lsi.shortened_url = c.shorten('http://%s%s' % (Site.objects.get_current().domain, lsi.content_object.get_absolute_url()))['url']
        lsi.save()
models.signals.post_save.connect(shorten_link, sender=LinkShortenedItem)
