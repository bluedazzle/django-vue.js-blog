from django.conf.urls import patterns, url
from api.views import ArticleDetailView, CommentView, LoginCallbackView, CommentListView, UserInfoView, ArticleListView, \
    ClassificationView, TagView, UploadView, TestView

urlpatterns = patterns('',
                       url(r'^articles', ArticleListView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)/comments$', CommentListView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)/comment$', CommentView.as_view()),
                       url(r'^article/(?P<aid>(\d)+)$', ArticleDetailView.as_view()),
                       url(r'^login/callback$', LoginCallbackView.as_view()),
                       url(r'^user/info$', UserInfoView.as_view()),
                       url(r'^tags$', TagView.as_view()),
                       url(r'^classifications', ClassificationView.as_view()),
                       url(r'^upload', UploadView.as_view()),
                       )
