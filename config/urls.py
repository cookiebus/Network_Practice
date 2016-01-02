from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^tags/', include('tags.urls')),
    url(r'^problems/', include('problems.urls')),
    url(r'^api/', include('api.urls')),
)
