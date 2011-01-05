from django import template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from urlr.models import *

class UrlrModelTests(TestCase):

    def setUp(self):
        a = User.objects.get_or_create(username='a')[0]

    def render(self, template_string, context={}):
        """Return the rendered string or the exception raised while rendering."""
        try:
            t = template.Template(template_string)
            c = template.Context(context)
            return t.render(c)
        except Exception, e:
            return e

    def test_model_and_shortening(self):
        lsi = LinkShortenedItem.objects.create(content_object=User.objects.all()[0])
        self.assertNotEqual(lsi.shortened_url, '')

        lsi2 = LinkShortenedItem.objects.for_object(User.objects.all()[0])
        self.assertEqual(lsi.pk, lsi2.pk)

    def test_filter(self):
        """This test is kinda fragile - it depends on you using my API key."""
        template = """{% load shorten_url %}{{ obj|shorten }}"""
        result = self.render(template, {'obj': User.objects.all()[0]})
        self.assertEqual(result, 'http://bit.ly/hh982R')

    def test_double_http(self):
        """In cases where the http:// is added to the site domain, links are getting http://http:// since the code auto-adds it blindly. I'm adding a method to determine the link and be aware of this."""
        s = Site.objects.get_current()

        self.assertEqual(determine_permalink(s, User.objects.all()[0].get_absolute_url()), 'http://example.com/users/a/')

        s.domain = 'http://%s' % s.domain # have to change it first. Django caches it the first time so if we want this to work it has to be set before being accessed
        s.save()

        self.assertEqual(determine_permalink(s, User.objects.all()[0].get_absolute_url()), 'http://example.com/users/a/')

        template = """{% load shorten_url %}{{ obj|shorten }}"""
        result = self.render(template, {'obj': User.objects.all()[0]}) # we want the same link - meaning the same input was sent and a double http:// was not
        self.assertEqual(result, 'http://bit.ly/hh982R')

        s.domain = s.domain[7:] # and put it back
        s.save()
