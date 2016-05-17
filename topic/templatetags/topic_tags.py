# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template
from django.utils.encoding import smart_text

from topic.models import Topic

register = template.Library()

@register.filter()
def get_topic_comment(topicid):
    topic = Topic.objects.get(id=topicid)
