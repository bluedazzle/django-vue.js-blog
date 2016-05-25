from django.conf.urls import patterns, include, url
from django.contrib import admin
from RaPo3 import settings

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'RaPo3.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('static_site.urls')),
                       url(r'^api/v1/', include('api.urls')),
                       url(r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA}),
                       )
