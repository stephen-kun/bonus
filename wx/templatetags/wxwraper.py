# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template
from django.utils.encoding import smart_text

register = template.Library()

@register.filter()
def wxurl_wraper(url):
    if not str(url).startswith('/wx'):
        return "/wx" + url