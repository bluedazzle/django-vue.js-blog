from django.conf.urls import patterns, url
from myadmin.views import *

urlpatterns = patterns('',
                       url(r'^login', LoginView.as_view()),
                       url(r'^logout', LogoutView.as_view()),
                       url(r'^info', AdminInfoView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)/publish', ArticlePublishView.as_view()),
                       url(r'^article', ModifyArticleView.as_view()),
                       url(r'^knowledge/(?P<kid>(\d)+)/publish', KnowledgePublishView.as_view()),
                       url(r'^knowledge', ModifyKnowledgeView.as_view()),
                       url(r'^comments', CommentListView.as_view()),
                       url(r'^collection/(?P<nid>(\d)+)', CollectionDetailView.as_view()),
                       url(r'^comment/(?P<aid>(\d)+)/review', ModifyKnowledgeView.as_view()),
                       url(r'^comment/(?P<aid>(\d)+)/delete', ModifyKnowledgeView.as_view()),
                       url(r'^comment/(?P<aid>(\d)+)/reply', ModifyKnowledgeView.as_view()),
                       )
