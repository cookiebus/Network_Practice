from django.conf.urls import patterns, url


urlpatterns = patterns(
    'users',
    url(r'^signin/$', 'views.signin'),
    url(r'^signup/$', 'views.signup')
)