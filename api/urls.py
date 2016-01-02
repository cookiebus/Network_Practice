from django.conf.urls import patterns, url


urlpatterns = patterns(
    'api',
    url(r'^profile/$', 'views.profile'),
    url(r'^problems/$', 'views.problems'),
    url(r'^myproblems/$', 'views.problems_with_user'),
    url(r'^user/(\d+)/$', 'views.user'),
    url(r'^problem/(\d+)/$', 'views.problem'),
    url(r'^comments/(\d+)/$', 'views.comments_with_problem')
)