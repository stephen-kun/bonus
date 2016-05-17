# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from topic.models import Topic
from .managers import CategoryQuerySet
from core.utils.models import AutoSlugField


class Category(models.Model):

    parent = models.ForeignKey('self', verbose_name=_("parent category"), null=True, blank=True)
    showimage = models.ImageField(verbose_name=_('show image'),upload_to='categoryimg',blank=True,null=True)

    title = models.CharField(_("title"), max_length=75)
    slug = AutoSlugField(populate_from="title", db_index=False, blank=True)
    description = models.CharField(_("description"), max_length=255, blank=True)
    is_global = models.BooleanField(_("global"), default=True,
                                    help_text=_('whether the topics will be '
                                                'displayed in the all-categories list.'))
    is_closed = models.BooleanField(_("closed"), default=False)
    is_removed = models.BooleanField(_("removed"), default=False)
    # is_private = models.BooleanField(_("private"), default=False)

    # topic_count = models.PositiveIntegerField(_("topic count"), default=0)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ['title', 'pk']
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def get_absolute_url(self):
        return reverse('category:detail', kwargs={'pk': str(self.id), 'slug': self.slug})

    @property
    def is_subcategory(self):
        if self.parent_id:
            return True
        else:
            return False

    @property
    def has_childrencategory(self):
        if Category.objects.filter(parent_id=self.pk).count()>0:
            return True
        else:
            return False

    def childrencategorys(self,obj):
        return Category.objects.filter(parent_id = obj.id)


    def getcount(self,parent_cat,today_min,today_max):
        num_topic = Topic.objects.filter(category_id = parent_cat.pk,date__range=(today_min,today_max)).count()
        if parent_cat.has_childrencategory:
            for childcat in self.childrencategorys(parent_cat):
                num_topic = self.getcount(childcat,today_min,today_max) + num_topic

        return num_topic

    @property
    def get_today_count(self):
        today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
        today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)

        num_topic = self.getcount(self,today_min,today_max)
        return num_topic

    def __unicode__(self):
        return self.slug


# def topic_posted_handler(sender, topic, **kwargs):
#    if topic.category.is_subcategory:
#        category = Category.objects.filter(pk__in=[topic.category.pk, topic.category.parent.pk])
#    else:
#        category = Category.objects.filter(pk=topic.category.pk)
#
#    category.update(topic_count=F('topic_count') + 1)


# topic_posted.connect(topic_posted_handler, dispatch_uid=__name__)
