from django import forms

from weixin.models import Consumer


class wxform(forms.Form):
    open_id = forms.CharField()

    class Meta:
        fields = ('open_id',)
