from django.conf.urls import patterns, url
from myadmin.views import *

urlpatterns = patterns('',
                       url(r'^login', LoginView.as_view()),
                       url(r'^logout', LogoutView.as_view()),
                       url(r'^info', AdminInfoView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)/publish', ArticlePublishView.as_view()),
                       url(r'^article', ModifyArticleView.as_view()),

                       )
