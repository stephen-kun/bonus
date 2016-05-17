# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class JoyForumUserAdminConfig(AppConfig):

    name = 'user.admin'
    verbose_name = _("JoyForum User Admin")
    label = 'user_admin'
