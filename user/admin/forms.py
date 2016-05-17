# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model

from ..models import Consumer

User = get_user_model()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "email", "is_active")


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Consumer
        fields = ("location", "localtimezone", "is_verified", "is_administrator", "is_moderator")