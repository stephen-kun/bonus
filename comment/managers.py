# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models import Q, Prefetch

from comment.like.models import CommentLike
from weixin.models import ConsumerGifts


class CommentQuerySet(models.QuerySet):

    def filter(self, *args, **kwargs):
        # TODO: find a better way
        return super(CommentQuerySet, self)\
            .filter(*args, **kwargs)\
            .select_related('user__jf')

    def unremoved(self):
        # TODO: remove action
        return self.filter(
            Q(topic__category__parent=None) | Q(topic__category__parent__is_removed=False),
            topic__category__is_removed=False,
            topic__is_removed=False,
            is_removed=False,
            action=0
        )

    # def public(self):
    #     return self.filter(topic__category__is_private=False)

    def visible(self):
        return self.unremoved()

    def for_topic(self, topic):
        return self.filter(topic=topic)

    def for_user(self,user,exclude=False):
        if not exclude:
            return self.filter(user = user)
        else:
            return self.exclude(user = user)

    def with_gifts(self,user):
        if not user.is_authenticated():
            return self

        user_gift = ConsumerGifts.objects.filter(user=user)
        prefetch = Prefetch("comment_gifts", queryset=user_gift, to_attr='gifts')
        return self.prefetch_related(prefetch)

    def with_likes(self, user):
        if not user.is_authenticated():
            return self

        user_likes = CommentLike.objects.filter(user=user)
        prefetch = Prefetch("comment_likes", queryset=user_likes, to_attr='likes')
        return self.prefetch_related(prefetch)


    def for_access(self, user):
        return self.unremoved()

    def for_update_or_404(self, pk, user):
        if user.jf.is_moderator:
            return get_object_or_404(self.for_access(user=user), pk=pk)
        else:
            return get_object_or_404(self.for_access(user), user=user, pk=pk)

    def after(self,dtime):
        return self.filter(date__gt=dtime)

    def before(self,dtime):
        return self.filter(date__lte=dtime)
