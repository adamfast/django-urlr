from django import template
from django.contrib.auth.models import User
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
        template = """{% load shorten_url %}{{ obj|shorten }}"""
        result = self.render(template, {'obj': User.objects.all()[0]})
        self.assertEqual(result, 'http://bit.ly/butJDd')
