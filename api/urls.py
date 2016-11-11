from django.conf.urls import patterns, url
from api.views import ArticleDetailView, CommentView, LoginCallbackView, CommentListView, UserInfoView, ArticleListView, \
    ClassificationView, TagView, UploadView, KnowListView, KnowDetailView, CollectionsListView

urlpatterns = patterns('',
                       url(r'^articles', ArticleListView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)/comments$', CommentListView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)/comment$', CommentView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)$', ArticleDetailView.as_view()),
                       url(r'^article/(?P<slug>([a-z0-9-])+)$', ArticleDetailView.as_view()),
                       url(r'^login/callback$', LoginCallbackView.as_view()),
                       url(r'^user/info$', UserInfoView.as_view()),
                       url(r'^tags$', TagView.as_view()),
                       url(r'^classifications', ClassificationView.as_view()),
                       url(r'^upload', UploadView.as_view()),
                       url(r'^knowledge/(?P<kid>(\d)+)$', KnowDetailView.as_view()),
                       url(r'^knowledge', KnowListView.as_view()),
                       url(r'^collections', CollectionsListView.as_view()),
                       )
