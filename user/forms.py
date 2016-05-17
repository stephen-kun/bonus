# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template import defaultfilters
from django.conf import settings

from weixin.models import Consumer

User = get_user_model()


class CleanEmailMixin(object):

    def clean_email(self):
        email = self.cleaned_data["email"]

        if settings.CASE_INSENSITIVE_EMAILS:
            email = email.lower()

        if not settings.UNIQUE_EMAILS:
            return email

        is_taken = User.objects\
            .filter(email=email)\
            .exists()

        if is_taken:
            raise forms.ValidationError(_("The email is taken."))

        return email

    def get_email(self):
        return self.cleaned_data["email"]


class EmailCheckForm(CleanEmailMixin, forms.Form):

    email = forms.CharField(label=_("Email"), widget=forms.EmailInput, max_length=254)


class EmailChangeForm(CleanEmailMixin, forms.Form):

    email = forms.CharField(label=_("Email"), widget=forms.EmailInput, max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not self.user.check_password(password):
            raise forms.ValidationError(_("The provided password is incorrect."))

        return password


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Consumer
        fields = ("location", "localtimezone")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        now = timezone.localtime(timezone.now())
        self.fields['localtimezone'].help_text = _('Current time is: %(date)s %(time)s') % {
            'date': defaultfilters.date(now),
            'time': defaultfilters.time(now)
        }
