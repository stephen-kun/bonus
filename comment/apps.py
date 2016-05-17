# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class JoyForumCommentConfig(AppConfig):

    name = 'comment'
    verbose_name = _("JoyForum Comment")
    label = 'comment'
