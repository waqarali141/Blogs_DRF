__author__ = 'waqarali'
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    url(r'^$', views.CategoryListing.as_view(), name='Category'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.PostsListing.as_view(), name='Post'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.CommentListing.as_view(), name='Post')

]

urlpatterns = format_suffix_patterns(urlpatterns)
