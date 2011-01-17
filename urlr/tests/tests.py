from django import template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase

from urlr.models import LinkShortenedItem
from urlr.tests.models import UrlrTestModel

class UrlrModelTests(TestCase):
    urls = 'urlr.tests.urls'
    
    def test_dummy(self):
        print 'hey'
