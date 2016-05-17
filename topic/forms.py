# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from djconfig.forms import ConfigForm

from core.utils.forms import NestedModelChoiceField
from category.models import Category
from .models import Topic


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('title', 'category')

    def __init__(self, user, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['category'] = NestedModelChoiceField(queryset=Category.objects.visible().opened(),
                                                         related_name='category_set',
                                                         parent_field='parent_id',
                                                         label_field='title',
                                                         label=_("Category"),
                                                         empty_label=_("Chose a category"))

        if self.instance.pk and not user.jf.is_moderator:
            del self.fields['category']

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user

        return super(TopicForm, self).save(commit)

class WXTopicForm(forms.ModelForm):
    title = forms.CharField(label=_("title"),widget=forms.TextInput(attrs={'placeholder':_('input topic title here.'),
                                                                           'style':"width:100%;height: 2rem;border: transparent;"}))

    class Meta:
        model = Topic
        fields = ('title',)

    def __init__(self, user, *args, **kwargs):
        super(WXTopicForm, self).__init__(*args, **kwargs)
        self.user = user
        # self.fields['category'] = NestedModelChoiceField(queryset=Category.objects.visible().opened(),
        #                                                  related_name='category_set',
        #                                                  parent_field='parent_id',
        #                                                  label_field='title',
        #                                                  label=_("Category"),
        #                                                  empty_label=_("Chose a category"))

        # if self.instance.pk and not user.jf.is_moderator:
        #     del self.fields['category']

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user

        return super(WXTopicForm, self).save(commit)

class BasicConfigForm(ConfigForm):

    site_name = forms.CharField(initial="JoyForum", label=_("site name"))
    site_description = forms.CharField(initial="", label=_("site description"), max_length=75, required=False)
    template_footer = forms.CharField(initial="", label=_("footer snippet"), required=False,
                                      widget=forms.Textarea(attrs={'rows': 2, }),
                                      help_text=_("This gets rendered just before the footer in your template."))
    comments_per_page = forms.IntegerField(initial=5, label=_("comments per page"), min_value=1, max_value=100)
    topics_per_page = forms.IntegerField(initial=5, label=_("topics per page"), min_value=1, max_value=100)
