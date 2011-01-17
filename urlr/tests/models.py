from django.core.urlresolvers import reverse
from django.db import models


class UrlrTestModel(models.Model):
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('urlr_test_view', args=[self.slug])
