# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone

from .models import Consumer


class TimezoneMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            timezone.activate(request.user.jf.localtimezone)
        else:
            timezone.deactivate()


class LastIPMiddleware(object):

    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        last_ip = request.META['REMOTE_ADDR'].strip()

        if request.user.jf.last_ip == last_ip:
            return

        Consumer.objects\
            .filter(user__pk=request.user.pk)\
            .update(last_ip=last_ip)


class LastSeenMiddleware(object):

    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        threshold = settings.USER_LAST_SEEN_THRESHOLD_MINUTES * 60
        delta = timezone.now() - request.user.jf.last_seen

        if delta.seconds < threshold:
            return

        Consumer.objects\
            .filter(user__pk=request.user.pk)\
            .update(last_seen=timezone.now())


class ActiveUserMiddleware(object):

    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        if not request.user.is_active:
            logout(request)