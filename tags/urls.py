from django.conf.urls import patterns, url
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'tags',
    url(r'^(\d+)/$', 'views.tags')
)