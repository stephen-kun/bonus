# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponsePermanentRedirect
from djconfig import config
from core.utils.paginator import paginate, yt_paginate
from core.utils.ratelimit.decorators import ratelimit
from category.models import Category
from comment.models import MOVED
from comment.forms import CommentForm
from comment.utils import comment_posted
from comment.models import Comment
from .models import Topic, SliderImage
from .forms import TopicForm
from . import utils


def group_required(function=None, groups=[], redirect_field_name=REDIRECT_FIELD_NAME, url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.groups.all().values_list("id", flat=True) in groups,
        login_url=url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@login_required
@ratelimit(rate='1/10s')
def publish(request, category_id=1):
    if category_id:
        get_object_or_404(Category.objects.visible(),
                          pk=category_id)

    if request.method == 'POST':
        form = TopicForm(user=request.user, data=request.POST)
        cform = CommentForm(user=request.user, data=request.POST)

        if not request.is_limited and all([form.is_valid(), cform.is_valid()]):  #
            # wrap in transaction.atomic?
            topic = form.save(commit=False)
            topic.category_id = 1
            topic.save()
            cform.topic = topic
            comment = cform.save()
            comment_posted(comment=comment, mentions=cform.mentions)
            return redirect(topic.get_absolute_url())
    else:
        form = TopicForm(user=request.user, initial={'category': category_id, })
        cform = CommentForm()

    context = {
        'form': form,
        'cform': cform
    }

    return render(request, 'forum/topic/publish.html', context)


@login_required
def update(request, pk):
    topic = Topic.objects.for_update_or_404(pk, request.user)

    if request.method == 'POST':
        form = TopicForm(user=request.user, data=request.POST, instance=topic)
        category_id = topic.category_id

        if form.is_valid():
            topic = form.save()

            if topic.category_id != category_id:
                Comment.create_moderation_action(user=request.user, topic=topic, action=MOVED)

            return redirect(request.POST.get('next', topic.get_absolute_url()))
    else:
        form = TopicForm(user=request.user, instance=topic)

    context = {'form': form, }

    return render(request, 'forum/topic/update.html', context)


# @group_required(groups=[1, 2], url="/nopermit/")
def detail(request, pk, slug):
    topic = Topic.objects.get_public_or_404(pk, request.user)

    if topic.slug != slug:
        return HttpResponsePermanentRedirect(topic.get_absolute_url())

    utils.topic_viewed(request=request, topic=topic)

    comments = Comment.objects \
        .for_topic(topic=topic) \
        .with_likes(user=request.user) \
        .with_gifts(user=request.user) \
        .order_by('date')

    comments = paginate(
        comments,
        per_page=config.comments_per_page,
        page_number=request.GET.get('page', 1)
    )

    context = {
        'topic': topic,
        'comments': comments,
        'time': time.time()
    }

    return render(request, 'forum/topic/detail.html', context)
    # return render(request, 'joyforum/categorydetail.html', context)


# @group_required(groups=[1, 2], url="/nopermit/")
def index_active(request):
    if request.user.is_authenticated() and Group.objects.get(id=3) in request.user.groups.all():
        return render(request, 'forum/topic/nopermit.html', {})

    categories = Category.objects \
        .visible() \
        .parents()

    topics = Topic.objects \
        .visible() \
        .global_() \
        .with_bookmarks(user=request.user) \
        .order_by('-is_globally_pinned', '-last_active') \
        .select_related('category')

    topics = yt_paginate(
        topics,
        per_page=config.topics_per_page,
        page_number=request.GET.get('page', 1)
    )

    sliderimages = SliderImage.objects.filter(enabled=True)

    context = {
        'categories': categories,
        'topics': topics,
        'sliderimages': sliderimages,
        'ctime': time.time()
    }

    return render(request, 'forum/topic/active.html', context)
    # return render(request,'joyforum/index.html',context)


def nopermit(request):
    return render(request, 'forum/topic/nopermit.html', {})
