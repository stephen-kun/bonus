# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class JoyForumCommentBookmarkConfig(AppConfig):

    name = 'comment.bookmark'
    verbose_name = _("JoyForum Comment Bookmark")
    label = 'comment.bookmark'
