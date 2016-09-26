from django.conf.urls import patterns, url
from static_site.views import *

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^email$', EmailView.as_view()),
                       url(r'^blog/(?P<aid>(\d)+)$', BlogView.as_view()),
                       url(r'^blog/(?P<slug>([a-z0-9-])+)$', BlogView.as_view()),
                       url(r'^blogs$', BlogListView.as_view(), name='blogs'),
                       url(r'^knowledge', KnowledgeListView.as_view(), name='knows'),
                       url(r'^about$', AboutView.as_view(), name='about'),
                       url(r'^admin/login$', AdminLoginView.as_view()),
                       url(r'^admin/index', AdminIndexView.as_view()),
                       url(r'^admin/comment', AdminCommentListView.as_view()),
                       url(r'^admin/article/new', AdminModifyArticleView.as_view()),
                       url(r'^admin/article/(?P<aid>(\d)+)$', AdminModifyArticleView.as_view()),
                       url(r'^admin/article', AdminArticleListView.as_view()),
                       url(r'^admin/knowledge/new$', AdminModifyKnowledgeView.as_view()),
                       url(r'^admin/knowledge/(?P<kid>(\d)+)$', AdminModifyKnowledgeView.as_view()),
                       url(r'^admin/knowledge', AdminKnowledgeListView.as_view()),

                       )
