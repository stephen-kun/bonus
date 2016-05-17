# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, include

import topic.moderate.urls
import topic.unread.urls
import topic.notification.urls
from . import views


urlpatterns = [
    url(r'^publish/$', views.publish, name='publish'),
    url(r'^publish/(?P<category_id>\d+)/$', views.publish, name='publish'),

    url(r'^update/(?P<pk>\d+)/$', views.update, name='update'),

    url(r'^(?P<pk>\d+)/$', views.detail, kwargs={'slug': "", }, name='detail'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.detail, name='detail'),

    url(r'^active/$', views.index_active, name='index-active'),

    url(r'^moderate/', include(topic.moderate.urls, namespace='moderate')),
    url(r'^unread/', include(topic.unread.urls, namespace='unread')),
    url(r'^notification/', include(topic.notification.urls, namespace='notification'))
]
