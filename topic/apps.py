# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig


class JoyForumTopicConfig(AppConfig):

    name = 'topic'
    verbose_name = "JoyForum Topic"
    label = 'topic'

    def ready(self):
        self.register_config()

    def register_config(self):
        import djconfig
        from .forms import BasicConfigForm

        djconfig.register(BasicConfigForm)