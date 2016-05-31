# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from comment.bookmark.models import CommentBookmark
from topic.models import TopicRead
from weixin.models import Consumer
from .notification.models import TopicNotification
from .unread.models import TopicUnread


User = get_user_model()


def topic_viewed(request, topic):
    # Todo test detail views
    user = request.user
    comment_number = CommentBookmark.page_to_comment_number(request.GET.get('page', 1))

    CommentBookmark.update_or_create(
        user=user,
        topic=topic,
        comment_number=comment_number
    )
    TopicNotification.mark_as_read(user=user, topic=topic)
    TopicUnread.create_or_mark_as_read(user=user, topic=topic)
    topic.increase_view_count()
    if user.jf.is_moderator or user.is_superuser:
        TopicRead.objects.create(topic=topic,user=user)
