from django.conf.urls import patterns, url
from static_site.views import *

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view()),
                       url(r'^blog/(?P<aid>(\d)+)$', BlogView.as_view()),
                       url(r'^blogs$', BlogListView.as_view()),
                       url(r'^about', AboutView.as_view()),
                       )
