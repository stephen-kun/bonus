# -*- coding: utf-8 -*-
import json
import time

import datetime
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponsePermanentRedirect, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string

from comment.forms import WXCommentForm, CommentForm
from comment.like.forms import LikeForm
from comment.like.models import CommentLike
from comment.utils import comment_posted
from core.utils import paginator
from core.utils import json_response
from core.utils import markdown
from core.utils.ratelimit.decorators import ratelimit
from djconfig import config

from category.models import Category
from comment.models import Comment, CommentImages
from topic.forms import TopicForm, WXTopicForm
from topic.models import Topic, SliderImage
from topic import  utils as topicutils
from core.utils.paginator import paginate, yt_paginate
from topic.notification.models import TopicNotification
from weixin.models import Consumer,ConsumerGifts



# def mylogin(request):
#     open_id = request.session.get('open_id',None)
#     if not open_id:
#         raise Http404(u'未获取到微信open_id！')
#
#     if request.user.is_anonymous():
#         user = authenticate(open_id=open_id)
#         login(request,user)
#     else:
#         if open_id != Consumer.objects.get(user=request.user).open_id:
#             logout(request)
#             user = authenticate(open_id=open_id)
#             login(request,user)


def wx_index(request, pk=1):
    category = get_object_or_404(Category.objects.visible(),pk=pk)
    if not request.is_ajax():
        open_id = request.GET.get('open_id',None)
        if request.user.is_anonymous():
            if not open_id:
                raise Http404(u'未获取到微信open_id！')

            get_object_or_404(Consumer.objects.all(),open_id=open_id)
            user = authenticate(open_id=open_id)
            login(request,user)
        else:
            if open_id and open_id != Consumer.objects.get(user=request.user).open_id:
                logout(request)
                user = authenticate(open_id=open_id)
                login(request,user)

        unread = TopicNotification.objects.for_access(request.user).unread().count()


        topics = Topic.objects\
            .unremoved()\
            .with_bookmarks(user=request.user)\
            .for_category(category=category,with_sub=False)\
            .order_by('-is_globally_pinned', '-is_pinned', '-last_active')\
            .select_related('category')

        maxitems = topics.count()

        showscroll = maxitems>config.topics_per_page

        topics = yt_paginate(
            topics,
            per_page=config.topics_per_page,
            page_number=request.GET.get('page', 1)
        )

        for topic in topics.object_list:
            comment = Comment.objects\
                .for_topic(topic=topic)\
                .with_likes(user=request.user)\
                .for_user(topic.user)\
                .order_by("date")
            topic.comment = comment[0]
            imagelist = CommentImages.objects.filter(comment = comment[0])
            topic.imagelist = imagelist
            giftscount = ConsumerGifts.objects.filter(comment = comment[0]).count()
            for commenti in Comment.objects.filter(topic=topic).exclude(id=comment[0].id):
                gifts = ConsumerGifts.objects.filter(comment = commenti)
                giftscount = giftscount + gifts.count()
            topic.gifts = giftscount

        sliderimages = SliderImage.objects.filter(enabled=True)

        context = {
            'category': category,
            # 'subcategories': subcategories,
            'topics': topics,
            'sliderimages':sliderimages,
            'time':time.time(),
            'curpage':topics.number,
            'maxitems':maxitems,
            'unread':unread,
            'showscroll':showscroll
        }

        # return render(request, 'forum/category/detail.html', context)
        # return render(request, 'joyforum/categorylist.html', context)
        return render(request,"joyforum/index.html",context)
    else:
        unread = TopicNotification.objects.for_access(request.user).unread().count()
        direction = request.POST.get("type","down")
        if direction == "down":
            pagetimestr = request.POST.get("ctime",None)
            pagetime = datetime.datetime.fromtimestamp(float(pagetimestr))
            topics = Topic.objects\
                .unremoved()\
                .with_bookmarks(user=request.user)\
                .for_category(category=category,with_sub=False)\
                .after(pagetime)\
                .order_by('-is_globally_pinned', '-is_pinned', '-last_active')\
                .select_related('category')

            count = topics.count()
            for topic in topics:
                comment = Comment.objects\
                    .for_topic(topic=topic)\
                    .with_likes(user=request.user)\
                    .for_user(topic.user)\
                    .order_by("date")
                topic.comment = comment[0]
                imagelist = CommentImages.objects.filter(comment = comment[0])
                topic.imagelist = imagelist
                giftscount = ConsumerGifts.objects.filter(comment = comment[0]).count()
                for commenti in Comment.objects.filter(topic=topic).exclude(id=comment[0].id):
                    gifts = ConsumerGifts.objects.filter(comment = commenti)
                    giftscount = giftscount + gifts.count()
                topic.gifts = giftscount
            context = {
                'time':time.time(),
                'count':count
            }
            htmlsnippet = render_to_string("joyforum/snippet/topic.html",{"topics":topics},context_instance=RequestContext(request))
            context.update({'html':htmlsnippet,'unread':unread})
            return json_response(context)
        else:
            pagetimestr = request.POST.get("ctime2",None)
            pagetime = datetime.datetime.fromtimestamp(float(pagetimestr))
            topics = Topic.objects\
                .unremoved()\
                .with_bookmarks(user=request.user)\
                .for_category(category=category,with_sub=False)\
                .before(pagetime)\
                .order_by('-is_globally_pinned', '-is_pinned', '-last_active')\
                .select_related('category')

            topics = yt_paginate(
                topics,
                per_page=config.topics_per_page,
                page_number=request.POST.get("page",2)
            )

            for topic in topics.object_list:
                comment = Comment.objects\
                    .for_topic(topic=topic)\
                    .with_likes(user=request.user)\
                    .for_user(topic.user)\
                    .order_by("date")
                topic.comment = comment[0]
                imagelist = CommentImages.objects.filter(comment = comment[0])
                topic.imagelist = imagelist
                giftscount = ConsumerGifts.objects.filter(comment = comment[0]).count()
                for commenti in Comment.objects.filter(topic=topic).exclude(id=comment[0].id):
                    gifts = ConsumerGifts.objects.filter(comment = commenti)
                    giftscount = giftscount + gifts.count()
                topic.gifts = giftscount

            htmlsnippet = render_to_string("joyforum/snippet/topic.html",{"topics":topics},context_instance=RequestContext(request))
            context={'html':htmlsnippet,'curpage':topics.number,'count':len(topics),'unread':unread}
            return json_response(context)



@ratelimit(rate='1/5s')
def wx_newtopic(request, category_id=1):
    if category_id:
        get_object_or_404(Category.objects.visible(),
                          pk=category_id)

    if request.method == 'POST':
        imagelist = request.POST.get("imagelist",None)
        form = WXTopicForm(user=request.user, data=request.POST)
        cform = WXCommentForm(user=request.user, data=request.POST)

        if not request.is_limited and all([form.is_valid(), cform.is_valid()]):  # TODO: test!
            # wrap in transaction.atomic?
            topic = form.save(commit=False)
            topic.category_id = 1
            topic.title = ""
            topic.save()
            cform.topic = topic
            comment = cform.save()
            for cmid in imagelist.split(","):
                try:
                    cimage = CommentImages.objects.get(id=cmid)
                    cimage.comment = comment
                    cimage.save()
                except Exception as ex:
                    print ex.args
            comment_posted(comment=comment, mentions=cform.mentions)
            return json_response({'url':topic.get_absolute_url(),'result':'ok'})
    else:
        form = WXTopicForm(user=request.user)
        cform = WXCommentForm()

    context = {
        'form': form,
        'cform': cform
    }
    return render(request,"joyforum/index_newtopic.html",context)

def wx_notification(request):
    if not request.is_ajax():
        maxitems = TopicNotification.objects.for_access(request.user).count()

        showscroll = maxitems>config.topics_per_page

        notifications = yt_paginate(
            TopicNotification.objects.for_access(request.user),
            per_page=config.topics_per_page,
            page_number=request.GET.get('page', 1)
        )

        unread = TopicNotification.objects.for_access(request.user).unread().count()

        context = {
                   'notifications': notifications,
                   'unread':unread,
                   'showscroll':showscroll,
                    'curpage':notifications.number,
                    'maxitems':maxitems,
                    'time':time.time()
        }
        return render(request,"joyforum/index_notification.html",context)
    else:
        direction = request.POST.get("type","down")
        if direction == "down":
            pagetimestr = request.POST.get("ctime",None)
            pagetime = datetime.datetime.fromtimestamp(float(pagetimestr))

            notifications = TopicNotification.objects\
                                .for_access(request.user)\
                                .after(pagetime)
            htmlsnippet = render_to_string("joyforum/snippet/notification.html",{"notifications":notifications},context_instance=RequestContext(request))
            context={'html':htmlsnippet,'time':time.time()}
            return json_response(context)

        else:
            pagetimestr = request.POST.get("ctime2",None)
            pagetime = datetime.datetime.fromtimestamp(float(pagetimestr))
            notifications = TopicNotification.objects\
                                .for_access(request.user)\
                                .before(pagetime)
            notifications = yt_paginate(
                notifications,
                per_page=config.topics_per_page,
                page_number=request.POST.get('page', 2)
            )
            htmlsnippet = render_to_string("joyforum/snippet/notification.html",{"notifications":notifications},context_instance=RequestContext(request))
            context={'html':htmlsnippet,'curpage':notifications.number,'count':len(notifications)}
            return json_response(context)

def wx_topic_detail(request, pk, slug):

    topic = Topic.objects.get_public_or_404(pk, request.user)
    topiccomment = Comment.objects\
                    .for_topic(topic=topic)\
                    .for_user(topic.user)\
                    .with_likes(user=request.user)\
                    .order_by("date")

    if not request.is_ajax():
        if topic.slug != slug:
            return HttpResponsePermanentRedirect(topic.get_absolute_url())

        topicutils.topic_viewed(request=request, topic=topic)

        topic.comment = topiccomment[0]

        comments = Comment.objects\
            .for_topic(topic=topic)\
            .order_by('-date')\
            .exclude(id=topiccomment[0].id)

        imagelist = CommentImages.objects.filter(comment = topiccomment[0])
        topic.imagelist = imagelist
        gifts = ConsumerGifts.objects.filter(comment = topiccomment[0])
        topic.gifts = gifts.count()

        maxitems = comments.count()

        showscroll = maxitems>config.comments_per_page

        comments = yt_paginate(
            comments,
            per_page=config.comments_per_page,
            page_number=request.GET.get('page', 1)
        )

        for comment in comments:
            imagelist = CommentImages.objects.filter(comment = comment)
            comment.imagelist = imagelist
            gifts = ConsumerGifts.objects.filter(comment = comment)
            comment.gifts = gifts.count()

        context = {
            'topic': topic,
            'comments': comments,
            'time':time.time(),
            'maxitems':maxitems,
            'curpage':comments.number,
            'showscroll':showscroll
        }
        return render(request, 'joyforum/categorydetail.html', context)

    else:
        direction = request.POST.get("type","down")
        if direction == "down":
            pagetimestr = request.POST.get("ctime",None)
            pagetime = datetime.datetime.fromtimestamp(float(pagetimestr))

            comments = Comment.objects\
                .for_topic(topic=topic)\
                .order_by('-date')\
                .after(pagetime)\
                .exclude(id=topiccomment[0].id)

            for comment in comments:
                imagelist = CommentImages.objects.filter(comment = comment)
                comment.imagelist = imagelist
                gifts = ConsumerGifts.objects.filter(comment = comment)
                comment.gifts = gifts.count()

            context = {
                'time':time.time()
            }

            htmlsnippet = render_to_string("joyforum/snippet/comment.html",{'comments': comments},context_instance=RequestContext(request))
            context.update({'html':htmlsnippet})
            return json_response(context)
        else:
            pagetimestr = request.POST.get("ctime2",None)
            pagetime = datetime.datetime.fromtimestamp(float(pagetimestr))
            comments = Comment.objects\
                .for_topic(topic=topic)\
                .order_by('-date')\
                .before(pagetime)\
                .exclude(id=topiccomment[0].id)

            comments = yt_paginate(
                comments,
                per_page=config.comments_per_page,
                page_number=request.POST.get('page', 2)
            )

            for comment in comments:
                imagelist = CommentImages.objects.filter(comment = comment)
                comment.imagelist = imagelist
                gifts = ConsumerGifts.objects.filter(comment = comment)
                comment.gifts = gifts.count()

            htmlsnippet = render_to_string("joyforum/snippet/comment.html",{'comments': comments},context_instance=RequestContext(request))
            context={'html':htmlsnippet,'curpage':comments.number,'count':len(comments)}
            return json_response(context)


def wx_login(request):
    next = request.GET.get("next",None)
    open_id = next.split('?')[1].split('=')[1]

    if not open_id:
        raise Http404(u'未获取到微信open_id！')

    get_object_or_404(Consumer.objects.all(),open_id=open_id)

    if request.user.is_anonymous():
        user = authenticate(open_id=open_id)
        login(request,user)
    else:
        if open_id != Consumer.objects.get(user=request.user).open_id:
            logout(request)
            user = authenticate(open_id=open_id)
            login(request,user)

    if request.session.get('open_id',None):
        if request.session['open_id']!=open_id:
            request.session['open_id'] = open_id

    else:
        request.session['open_id'] = open_id
    #
    #
    return HttpResponseRedirect('/wx/')


def wx_comment_like_create(request,comment_id):

    open_id = request.user.jf.open_id

    wxuser = Consumer.objects.get(open_id = open_id )

    comment = get_object_or_404(Comment.objects.exclude(user=wxuser.user), pk=comment_id)

    if request.method == 'POST':
        form = LikeForm(user=wxuser.user, comment=comment, data=request.POST)

        if form.is_valid():
            like = form.save()
            like.comment.increase_likes_count()

            if request.is_ajax():
                return json_response({'url_delete': like.get_wx_delete_url()})

            return redirect(request.POST.get('next', comment.get_absolute_url()))
    else:
        form = LikeForm()

    context = {
        'form': form,
        'comment': comment
    }

    return render(request, 'forum/comment/like/create.html', context)


def wx_comment_like_delete(request,pk):

    open_id = request.user.jf.open_id

    wxuser = Consumer.objects.get(open_id = open_id)

    like = get_object_or_404(CommentLike, pk=pk, user=wxuser.user)

    if request.method == 'POST':
        like.delete()
        like.comment.decrease_likes_count()

        if request.is_ajax():
            url = reverse('wx:wx-comment-like-create', kwargs={'comment_id': like.comment.pk, })
            return json_response({'url_create': url, })

        return redirect(request.POST.get('next', like.comment.get_absolute_url()))

    context = {'like': like, }

    return render(request, 'forum/comment/like/delete.html', context)


@ratelimit(rate='1/10s')
def wx_comment_publish(request, topic_id, pk=None):
    topic = get_object_or_404(
        Topic.objects.opened().for_access(request.user),
        pk=topic_id
    )

    if request.method == 'POST':
        form = WXCommentForm(user=request.user, topic=topic, data=request.POST)

        if not request.is_limited and form.is_valid():
            comment = form.save()
            comment_posted(comment=comment, mentions=form.mentions)
            # return redirect(request.POST.get('next', comment.get_absolute_url()))
            # htmlcontext = {
            #             'comment':comment
            #            }
            # html = render_to_string("joyforum/catlist/comment_snippet.html",htmlcontext,context_instance=RequestContext(request))
            # context = {'result':'ok','html':html}
            context = {'result':'ok'}
            return json_response(context)
        else:
            return json_response({'result':'nok','errorinfo':"评论太频繁，请稍后再试！"})

    else:
        initial = None

        if pk:
            comment = get_object_or_404(Comment.objects.for_access(user=request.user), pk=pk)
            quote = markdown.quotify(comment.comment, comment.user.username)
            initial = {'comment': quote, }

        form = WXCommentForm(initial=initial)

    context = {
        'form': form,
        'topic': topic
    }

    return render(request, 'joyforum/comment.html', context)


def wx_comment_find(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment_number = Comment.objects.filter(topic=comment.topic, date__lte=comment.date).count()
    # url = paginator.get_url(comment.topic.get_absolute_url(),
    #                         comment_number,
    #                         config.comments_per_page,
    #                         'page')
    url = comment.topic.get_absolute_url()
    return redirect('/wx'+url)
