__author__ = 'waqarali'
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='Index'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.PostIndexView.as_view(), name='Post')
]

urlpatterns = format_suffix_patterns(urlpatterns)
