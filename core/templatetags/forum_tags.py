# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from comment import tags as comment
from comment.like import tags as like
# from search import tags as search
from topic.notification import tags as topic_notification

from ..tags import avatar
from ..tags import gravatar
from ..tags import messages
from ..tags import paginator
from ..tags import social_share
from ..tags import time
from ..tags import urls
from ..tags.registry import register


__all__ = [
    'comment',
    'like',
    # 'search',
    'topic_notification',
    'avatar',
    'gravatar',
    'messages',
    'paginator',
    'social_share',
    'time',
    'urls',
    'register'
]
