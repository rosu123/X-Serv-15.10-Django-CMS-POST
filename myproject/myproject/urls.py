from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', login),
    url(r'^logout', 'cms_post.views.mylogout'),
    url(r'^$', 'cms_post.views.barra'),
    url(r'^(\d+)', 'cms_post.views.content'),
    url(r'^annotated/$', 'cms_post.views.barraAnnotated'),
    url(r'^annotated/(\d+)', 'cms_post.views.contentAnnotated'),
    url(r'^(.*)', 'cms_post.views.msg_error'),
]
