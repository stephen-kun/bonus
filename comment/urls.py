# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, include

import comment.bookmark.urls
import comment.history.urls
import like.urls
from . import views


urlpatterns = [
    url(r'^(?P<topic_id>\d+)/publish/$', views.publish, name='publish'),
    url(r'^(?P<topic_id>\d+)/publish/(?P<pk>\d+)/quote/$', views.publish, name='publish'),

    url(r'^(?P<pk>\d+)/update/$', views.update, name='update'),
    url(r'^(?P<pk>\d+)/find/$', views.find, name='find'),
    url(r'^(?P<topic_id>\d+)/move/$', views.move, name='move'),

    url(r'^(?P<pk>\d+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<pk>\d+)/undelete/$', views.delete, kwargs={'remove': False, }, name='undelete'),
    # url(r'^like/(?P<comment_id>\d+)/create/$',views.commentlike,name='commentlike'),
    # url(r'^like/(?P<pk>\d+)/delete/$', views.commentlikedelete, name='commentlikedelete'),
    url(r'^addgift/(?P<cid>\d+)/$',views.addgift,name='addgift'),

    url(r'^upload/$', views.image_upload_ajax, name='image-upload-ajax'),

    url(r'^bookmark/', include(comment.bookmark.urls, namespace='bookmark')),
    url(r'^history/', include(comment.history.urls, namespace='history')),
    url(r'^like/', include(like.urls, namespace='like')),
]
