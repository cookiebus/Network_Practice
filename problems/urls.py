from django.conf.urls import patterns, url


urlpatterns = patterns(
    'problems',
    url(r'^post/$', 'views.create')
)