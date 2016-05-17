# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class JoyForumCommentHistoryConfig(AppConfig):

    name = 'comment.history'
    verbose_name = _("JoyForum Comment History")
    label = 'comment.history'
