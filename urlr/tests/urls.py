from django.core.urlresolver.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', lambda request, slug: None, name='urlr_test_view'),
)
