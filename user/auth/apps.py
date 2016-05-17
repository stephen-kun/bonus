# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class JoyForumUserAuthConfig(AppConfig):

    name = 'user.auth'
    verbose_name = _("JoyForum User Auth")
    label = 'user_auth'
