# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class JoyForumNotificationConfig(AppConfig):

    name = 'topic.notification'
    verbose_name = _("JoyForum Topic Notification")
    label = 'topic.notification'
