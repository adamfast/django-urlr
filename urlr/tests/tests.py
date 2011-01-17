from django import template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils.hashcompat import md5_constructor

from urlr.models import bitly, LinkShortenedItem
from urlr.tests.models import UrlrTestModel


def _short_url(url):
    return 'http://bit.ly/%s' % md5_constructor(url).hexdigest()

def monkeypatch(url):
    return {'url': _short_url(url)}

class UrlrModelTests(TestCase):
    urls = 'urlr.tests.urls'
    
    def setUp(self):
        # monkeypatch the bitly_api shorten function
        self.orig_shorten = bitly.shorten
        bitly.shorten = monkeypatch
        
        # create a couple test objects
        self.test_a = UrlrTestModel.objects.create(slug='a')
        self.test_b = UrlrTestModel.objects.create(slug='b')
    
    def tearDown(self):
        bitly.shorten = self.orig_shorten
    
    def assertUrlsEqual(self, long_url, short_url):
        return self.assertEqual(_short_url(long_url), short_url)
    
    def test_shortening(self):
        self.assertRaises(
            LinkShortenedItem.DoesNotExist,
            LinkShortenedItem.objects.for_object,
            self.test_a
        )
        
        obj, c = LinkShortenedItem.objects.get_or_create_for_object(self.test_a)
        self.assertTrue(c)
        self.assertUrlsEqual(
            'http://example.com/a/', obj.shortened_url
        )
        
        obj, c = LinkShortenedItem.objects.get_or_create_for_object(self.test_a)
        self.assertFalse(c)
        self.assertUrlsEqual(
            'http://example.com/a/', obj.shortened_url
        )
        
        obj, c = LinkShortenedItem.objects.get_or_create_for_object(self.test_b)
        self.assertTrue(c)
        self.assertUrlsEqual(
            'http://example.com/b/', obj.shortened_url
        )
