# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig


class JoyForumUserConfig(AppConfig):

    name = 'user'
    verbose_name = "JoyForum User"
    label = 'user'

    def ready(self):
        self.register_signals()

    def register_signals(self):
        from . import signals
