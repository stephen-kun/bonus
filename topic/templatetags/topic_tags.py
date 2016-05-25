# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import truncatewords, stringfilter
from django.utils.encoding import smart_text
from django.utils.html import *
from django.utils.text import *

from topic.models import Topic

register = template.Library()

@register.filter()
def get_topic_comment(topicid):
    topic = Topic.objects.get(id=topicid)


@register.filter(is_safe=False)
@stringfilter
def mytruncatewords(value, arg):
    try:
        value = strip_tags(value)
        length = int(arg)
    except ValueError:  # Invalid literal for int().
        return value  # Fail silently.
    return Truncator(value).words(length, truncate=' ...')
