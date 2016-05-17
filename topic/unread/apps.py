# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class TopicUnreadConfig(AppConfig):

    name = 'topic.unread'
    verbose_name = _("JoyForum Topic Unread")
    label = 'topic.unread'
