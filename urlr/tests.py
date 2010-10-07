from django.contrib.auth.models import User
from django.test import TestCase
from urlr.models import *

class UrlrModelTests(TestCase):

    def setUp(self):
        a = User.objects.get_or_create(username='a')[0]

    def test_model_and_shortening(self):
        lsi = LinkShortenedItem.objects.create(content_object=User.objects.all()[0])
        self.assertNotEqual(lsi.shortened_url, '')

        lsi2 = LinkShortenedItem.objects.for_object(User.objects.all()[0])
        self.assertEqual(lsi.pk, lsi2.pk)
