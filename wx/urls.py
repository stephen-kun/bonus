# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, include

from . import views


urlpatterns = [
    # url(r'^publish/$', views.publish, name='publish'),
    # url(r'^publish/(?P<category_id>\d+)/$', views.publish, name='publish'),
    #
    # url(r'^update/(?P<pk>\d+)/$', views.update, name='update'),
    #
    # url(r'^(?P<pk>\d+)/$', views.detail, kwargs={'slug': "", }, name='detail'),
    # url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.detail, name='detail'),

    url(r'^$', views.wx_index, name='wx-index'),
    url(r'^wx_notification/$',views.wx_notification,name='wx-notification'),
    url(r'^wx_newtopic/$',views.wx_newtopic,name='wx-newtopic'),
    url(r'^wxlogin/$',views.wx_login,name='wx-login'),
    # url(r'^category/(?P<pk>\d+)/$', views.wx_category_detail, kwargs={'slug': "", }, name='wx-category-detail'),
    # url(r'^category/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.wx_category_detail, name='wx-category-detail'),

    url(r'^topic/(?P<pk>\d+)/$', views.wx_topic_detail, kwargs={'slug': "", }, name='wx-topic-detail'),
    url(r'^topic/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.wx_topic_detail, name='wx-topic-detail'),
    url(r'^comment/like/(?P<comment_id>\d+)/create/$',views.wx_comment_like_create,name='wx-comment-like-create'),
    url(r'^comment/like/(?P<pk>\d+)/delete/$',views.wx_comment_like_delete,name='wx-comment-like-delete'),
    url(r'^comment/(?P<topic_id>\d+)/publish/$',views.wx_comment_publish,name='wx-comment-publish'),
    url(r'^comment/(?P<pk>\d+)/find/$', views.wx_comment_find, name='wx-comment-find'),
]
