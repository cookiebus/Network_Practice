from django.conf.urls import patterns, url


urlpatterns = patterns(
    'api',
    url(r'^userprofile/(\d+)/$', 'views.userprofile'),
    url(r'^profile/$', 'views.profile'),
    url(r'^problems/(\d+)/$', 'views.problems'),
    url(r'^myproblems/(\d+)/$', 'views.problems_with_user'),
    url(r'^user/(\d+)/$', 'views.user'),
    url(r'^problem/(\d+)/$', 'views.problem'),
    url(r'^comments/(\d+)/$', 'views.comments_with_problem'),
    url(r'^signin/$', 'views.signin'),
    url(r'^signup/$', 'views.signup'),
    url(r'^post_problem/$', 'views.post_problem'),
    url(r'^post_tag/$', 'views.post_tag'),
    url(r'^post_comment/$', 'views.post_comment'),
    url(r'^post_profile/(\d+)/$', 'views.post_profile'),
    url(r'^favorite/$', 'views.favorite'),
    url(r'^unfavorite/$', 'views.unfavorite'),
    url(r'^is_favorite/$', 'views.is_favorite'),
    url(r'^myfavorite/(\d+)/$', 'views.myfavorite')
)
