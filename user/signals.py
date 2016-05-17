# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from weixin.models import Consumer

User = get_user_model()


def update_or_create_user_profile(sender, instance, created, **kwargs):
    user = instance

    if created:
        Consumer.objects.create(user=user)
    else:
        user.jf.save()

post_save.connect(update_or_create_user_profile, sender=User, dispatch_uid=__name__)
