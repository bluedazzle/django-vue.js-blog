from django.conf.urls import patterns, url
from weapp.views import *

urlpatterns = patterns('',
                       url(r'^auth', WeAppAuthView.as_view()),
                       url(r'^search', SearchView.as_view()),
                       url(r'^check', UserCheckView.as_view()),
                       url(r'^domains', DomainListView.as_view()),
                       url(r'^domain/(?P<did>(\d)+)', DomainHandleView.as_view()),
                       )
