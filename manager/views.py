# -*- coding:utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, \
	HttpResponsePermanentRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from core.utils import markdown,paginator
from core.utils.decorators import moderator_required
from djconfig import config

from category.models import Category
from comment.forms import CommentForm
from comment.models import CommentImages, Comment
from comment.utils import comment_posted
from core.utils.paginator import paginate, yt_paginate
from core.utils.ratelimit.decorators import ratelimit
from topic.forms import TopicForm
from topic.models import Topic, SliderImage, TopicRead
from  weixin.models import *
# from  weixin.models import DiningTable,VirtualMoney, SndBonus, RcvBonus, WalletMoney, Consumer, Recharge, Ticket
from weixin import utils
from topic import utils as utils2
import datetime
import time
from manager.utils import *
from manager.models import *


def gen_id():
	return utils.create_primary_key()


def get_admin_account():
	return Consumer.objects.get(open_id='0001')


@login_required(login_url='/manager/login/')
def index(request):
	current_user = request.user
	return render_to_response("manager/account/account.html")


def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/manager/account/")


# 红包统计信息
@login_required(login_url='/manager/login/')
def bonus_info(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False
	return render_to_response("manager/bonus/bonus_info.html", locals())


def send_bonus_list(request):
	today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
	today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
	bonus_list = SndBonus.objects.filter(create_time__range=(today_min, today_max)).order_by('create_time')
	return render_to_response("manager/bonus/snd_bonus_list.html", {'title': '发出的红包', 'bonus_list': bonus_list})


def recv_bonus_list(request):
	today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
	today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
	bonus_list = RcvBonus.objects.filter(datetime__range=(today_min, today_max), is_receive=True)
	return render_to_response("manager/bonus/recv_bonus_list.html", {'bonus_list': bonus_list})


def flying_bonus_list(request):
	time = datetime.datetime.today()
	start_date = datetime.datetime(time.year,time.month,time.day,0,0,0,tzinfo=timezone.get_current_timezone())
	end_date = start_date + datetime.timedelta(1) 
	bonus_list = SndBonus.objects.filter(is_exhausted=False, create_time__range=(start_date, end_date)).order_by(
		'create_time')
	return render_to_response("manager/bonus/flying_bonus_list.html", {'bonus_list': bonus_list})


def create_bonus(request):
	current_user = request.user
	good_list = VirtualMoney.objects.all()
	return render_to_response("manager/bonus/create_bonus.html", {'good_list': good_list})


@csrf_exempt
def create_bonus_action(request):
	title = request.POST.get("title")
	message = request.POST.get("message")
	counter = int(request.POST.get("counter"))
	good_list = VirtualMoney.objects.all()
	total_money = 0
	total_counter = 0
	good_contents = {}
	for good in good_list:
		good_counter = int(request.POST.get(good.name))
		good_contents[good.name] = good_counter
		total_counter = total_counter + good_counter
		total_money = total_money + good_counter * good.price

	if (total_counter < counter):
		return _response_json(1, u"确认物品数量总和大于红包数!")

	if (total_money == 0):
		return _response_json(1, u"红包没有内容!")

	(success, err) = check_account_limit(good_contents)
	if (not success):
		return _response_json(1, err)
	else:
		get_admin_account().send_sys_bonus(counter=counter, good_contents=good_contents, title=title, message=message)
		return _response_json(0, u"红包发送成功!")


def bonus_detail(request):
	bonus_type = request.GET.get('type')
	id = request.GET.get('bonus_id')
	good_list = VirtualMoney.objects.all()
	content = ""
	remain_content = ""
	if (bonus_type == 'system' or bonus_type == 'send'):
		try:
			bonus = SndBonus.objects.get(id_bonus=id)
			for good in good_list:
				wm_list = WalletMoney.objects.filter(snd_bonus=bonus, money=good)
				counter = 0
				remain_counter = 0
				for w in wm_list:
					counter += 1
					if not w.is_receive:
						remain_counter += 1

				if (counter > 0):
					content = content + ("%d%s%s," % (counter, good.unit, good.name))

				if (remain_counter > 0):
					remain_content = remain_content + ("%d%s%s," % (remain_counter, good.unit, good.name))

			recv_bonus_list = RcvBonus.objects.filter(snd_bonus=bonus, consumer__isnull=False)
			return render_to_response("manager/bonus/bonus_detail.html",
									  {'bonus': bonus, 'recv_bonus_list': recv_bonus_list, 'content': content,
									   'remain_content': remain_content})

		except ObjectDoesNotExist:
			return render_to_response("manager/bonus/bonus_detail.html")

	elif (bonus_type == 'recv'):
		recv_bonus_list = RcvBonus.objects.filter(id_bonus=id)
		bonus = recv_bonus_list[0].snd_bonus
		return render_to_response("manager/bonus/bonus_detail.html",
								  {'bonus': bonus, 'recv_bonus_list': recv_bonus_list, 'content': content,
								   'remain_content': remain_content})
	else:
		return render_to_response("manager/bonus/bonus_detail.html")


# 判断发送的红包是否超额
def check_account_limit(good_contents):
	admin = get_admin_account()
	for name, number in good_contents.items():
		if number > admin.get_valid_good_number_by_name(name):
			return False, u"帐户%s数量不足！" % name

	return True, "Success!"


def sys_bonus_list(request):
	bonus_list = SndBonus.objects.filter(bonus_type=2)
	return render_to_response("manager/bonus/sys_bonus_list.html", {"bonus_list": bonus_list})


# 管理者信息
@login_required(login_url='/manager/login/')
def account(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False

	return render_to_response("manager/account/account.html", {'current_user': current_user, 'is_admin': is_admin})


def bonus_rank_list(request):
	consumer_list = Consumer.objects.exclude(open_id='0001').order_by("rcv_bonus_num").reverse()
	return render_to_response('manager/bonus/bonus_rank_list.html', {'consumer_list': consumer_list})


def sys_account_detail(request):
	consumer = Consumer.objects.get(open_id='0001')
	return render_to_response("manager/account/sys_account.html", {'consumer': consumer})


def account_manage(request):
	user_list = User.objects.filter(groups__name='manager', is_active=True)
	return render_to_response("manager/account/manage_account.html", {'user_list': user_list})


def account_create(request):
	current_user = request.user
	return render_to_response("manager/account/create_account.html", {'current_user': current_user})


def _response_json(state, message):
	data = {}
	data['state'] = state
	data['message'] = message
	return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def action(request):
	action = request.POST.get("action")
	if (action == "register"):
		username = request.POST.get("username")
		password = request.POST.get("password")
		if Consumer.create_manager(username, password):
			return _response_json(0, u"新增用户%s" % (username))
		else:
			return _response_json(1, u"用户名已存在!")
			
	elif (action == "delete"):
		username = request.POST.get("username")
		try:
			user = User.objects.get(username=username)
			user.is_active = False
			user.save()
			return _response_json(0, u"删除成功!")
		except ObjectDoesNotExist:
			return _response_json(0, u"删除成功!")
	elif (action == "modify_password"):
		username = request.POST.get("username")
		if (request.user.username != "admin"):
			username = request.user.username
			password = request.POST.get("password")
			if password is None:
				return _response_json(1, u"密码不正确!")
			user = authenticate(username=username, password=password)
			if user is None:
				return _response_json(1, u"密码不正确!")

		new_password = request.POST.get("new_password")
		u = User.objects.get(username=username)
		u.set_password(new_password)
		u.save()
		return _response_json(0, u"修改密码成功!")
	elif (action == "limit_bonus"):
		good_list = VirtualMoney.objects.all()
		admin = get_admin_account()
		kw = {}
		for good in good_list:
			counter = int(request.POST.get(good.name))
			kw[good.name] = counter

		admin.account_charge(kw)

		return _response_json(0, u"设置成功!")
	elif (action == "limit_coupon"):
		admin = get_admin_account()
		counter = int(request.POST.get('counter'))
		val = int(request.POST.get('value'))
		print counter, val
		for i in range(counter):
			Ticket.objects.create(id_ticket=gen_id(), ticket_type=1, ticket_value=val, consumer=admin)
		return _response_json(0, u"设置成功!")
	else:
		return _response_json(1, u"错误操作")


def change_password(request):
	current_user = request.user
	return render_to_response("manager/account/change_password.html", {'current_user': current_user})


def set_coupon_limit(request):
	current_user = request.user
	return render_to_response("manager/account/set_coupon_limit.html")


def set_bonus_limit(request):
	current_user = request.user
	good_list = VirtualMoney.objects.all()
	return render_to_response("manager/account/set_bonus_limit.html", {'good_list': good_list})


# 就餐信息
@login_required(login_url='/manager/login/')
def dining(request):
	current_user = request.user
	return render_to_response("manager/dining/dining.html", {'current_user': current_user})


def dining_list(request):
	current_user = request.user
	return render_to_response("manager/dining/dining_list.html")


# 店内基本信息
def basic(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False
	return render_to_response("manager/basic/index.html", locals())

def check_ticket(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False
	return render_to_response("manager/basic/admin_check_ticket.html", locals())


def delete_account(request):
	current_user = request.user
	return render_to_response("manager/basic/delete.html")


def create_coupon(request):
	current_user = request.user
	return render_to_response("manager/basic/create_coupon.html")


def send_coupon(request):
	return _response_json(0, "success!")


def goods_info(reqeust):
	good_list = VirtualMoney.objects.all()
	return render_to_response("manager/basic/goods_info.html", {"good_list": good_list})


def good_item_edit(request):
	id = request.GET.get("good_id")
	if (id):
		action = "edit"
		try:
			good = VirtualMoney.objects.get(id=id)
		except ObjectDoesNotExist:
			good = None
			action = "add"
	else:
		good = None
		action = "add"

	return render_to_response("manager/basic/add_edit_good.html", {'action': action, 'good': good})


@csrf_exempt
def good_action(request):
	action = request.POST.get("action")
	if (action == 'add'):
		name = request.POST.get('good_name')
		price = request.POST.get('good_price')
		unit = request.POST.get('good_unit')
		try:
			good = VirtualMoney.objects.get(name=name)
			return _response_json(1, u"已有相同名字类别!")
		except ObjectDoesNotExist:
			id = gen_id()
			good = VirtualMoney.objects.create(id=id, name=name, price=price, unit=unit)
			good.save()
			return _response_json(0, u"添加成功!")

	elif (action == 'edit'):
		id = request.POST.get('good_id')
		name = request.POST.get('good_name')
		price = request.POST.get('good_price')
		unit = request.POST.get('good_unit')
		try:
			VirtualMoney.objects.filter(id=id).update(name=name, price=price, unit=unit)
			return _response_json(0, u"修改成功!")
		except ObjectDoesNotExist:
			return _response_json(1, u"不存在的数据！")

	elif (action == 'delete'):
		id = request.POST.get('good_id')
		print(id)
		VirtualMoney.objects.filter(id=id).delete()
		return _response_json(0, u"删除成功!")
	else:
		return _response_json(1, u"错误操作!")


def tables_info(request):
	table_list = DiningTable.objects.all()
	return render_to_response("manager/basic/tables_info.html", {'table_list': table_list})


def table_item_edit(request):
	action = "add"
	index = request.GET.get("index_table")
	if (index):
		try:
			action = "edit"
			table = DiningTable.objects.get(index_table=index)
		except ObjectDoesNotExist:
			table = None
			action = "add"
	else:
		action = "add"
		table = None
	return render_to_response("manager/basic/add_edit_table.html", {'action': action, 'table': table})


@csrf_exempt
def table_action(request):
	# print(request.body)
	action = request.POST.get("action")
	if (action == 'add'):
		index = request.POST.get("table_num")
		cap = request.POST.get("capacity")
		if (request.POST.get("is_vip") == '1'):
			is_vip = True
		else:
			is_vip = False

		try:
			DiningTable.objects.get(index_table=index)
			return _response_json(1, u"桌号已存在!")
		except ObjectDoesNotExist:
			table = DiningTable.objects.create(index_table=index, seats=int(cap), is_private=is_vip)
			table.save()
			return _response_json(0, u"增加成功!")
	elif (action == "delete"):
		index = request.POST.get("table_num")
		DiningTable.objects.filter(index_table=index).delete()
		return _response_json(0, u"删除成功!")
	elif (action == "edit"):
		index = request.POST.get("table_num")
		cap = request.POST.get("capacity")
		if (request.POST.get("is_vip") == '1'):
			is_vip = True
		else:
			is_vip = False
		DiningTable.objects.filter(index_table=index).update(seats=cap, is_private=is_vip)
		return _response_json(0, u"编辑成功!")
	else:
		return _response_json(1, u"错误操作!")


@login_required(login_url='/manager/login/')
def consumer_index(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False

	return render_to_response("manager/consumer/index.html", {'current_user': current_user, 'is_admin': is_admin})


@login_required(login_url='/manager/login/')
def consumer_list(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False
	date_str = request.GET.get("date")
	if (date_str):
		time = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
	else:
		time = datetime.datetime.today()
	consumer_list = Consumer.get_consumers_by_dining_date(time)
	return render_to_response("manager/consumer/consumer_list.html",
							  {'current_user': current_user, 'is_admin': is_admin, 'time': time,
							   'consumer_list': consumer_list})


def dining_list(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False
	date_str = request.GET.get("date")
	if (date_str):
		time = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
	else:
		time = datetime.datetime.today()
	session_set = DiningSession.get_sessions_by_dining_date(time)
	print session_set
	return render_to_response("manager/consumer/dining_list.html",
							  {'current_user': current_user, 'is_admin': is_admin, 'time': time,
							   'sessions': session_set})


@login_required(login_url='/manager/login/')
def consumer_is_dining(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False

	session_list = DiningSession.objects.filter(over_time__isnull=True)
	print session_list
	return render_to_response("manager/consumer/consumer_is_dining.html",
							  {'current_user': current_user, 'is_admin': is_admin, 'session_list': session_list})


def dining_session_detail(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False

	index_table = request.GET.get('table_index')
	table = DiningTable.objects.get(index_table=index_table)
	session = DiningSession.objects.filter(table=table).latest('begin_time')
	return render_to_response("manager/consumer/dining_session_detail.html",
							  {'current_user': current_user, 'is_admin': is_admin, 'session': session})


def consumer_detail(request):
	open_id = request.GET.get('open_id')
	try:
		consumer = Consumer.objects.get(open_id=open_id)
		return render_to_response("manager/consumer/consumer_detail.html", {'consumer': consumer})
	except ObjectDoesNotExist:
		return render_to_response("manager/consumer/consumer_detail.html")


def consumer_bonus_list(request):
	open_id = request.GET.get('open_id')
	consumer = Consumer.objects.get(open_id=open_id)
	bonus_type = request.GET.get('bonus_type')
	if (bonus_type == 'send'):
		bonus_list = SndBonus.objects.filter(consumer=consumer)
		bonus_num = len(bonus_list)
		return render_to_response("manager/consumer/consumer_send_bonus_list.html",
								  {'consumer': consumer, 'bonus_list': bonus_list, 'bonus_num': bonus_num})
	else:
		bonus_list = RcvBonus.objects.filter(consumer=consumer)
		bonus_num = len(bonus_list)
		return render_to_response("manager/consumer/consumer_recv_bonus_list.html",
								  {'consumer': consumer, 'bonus_list': bonus_list, 'bonus_num': bonus_num})


@login_required(login_url='/manager/login/')
def statistics_index(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False

	return render_to_response("manager/statistics/index.html", {'current_user': current_user, 'is_admin': is_admin})


@login_required(login_url='/manager/login/')
def daily_statistics(request):
	request_type = request.GET.get('type')
	if request_type == "consumers":
		is_admin = False
	else:
		is_admin = True

	date_str = request.GET.get('date')
	if (date_str):
		try:
			time = datetime.datetime.strptime(date_str, "%Y-%m-%d")
		except ValueError:
			time = datetime.datetime.today()
	else:
		time = datetime.datetime.today()

	daily_statistics = get_daily_statistics(time, is_admin)
	return render_to_response("manager/statistics/sys_daily_statistics.html", {'daily_statistics': daily_statistics})


@login_required(login_url='/manager/login/')
def daily_detail(request):
	request_type = request.GET.get('type')
	if request_type == "consumers":
		is_admin = False
	else:
		is_admin = True

	date_str = request.GET.get('date')
	if (date_str):
		try:
			time = datetime.datetime.strptime(date_str, "%Y-%m-%d")
		except ValueError:
			time = datetime.datetime.today()
	else:
		time = datetime.datetime.today()

	daily_detail = get_daily_detail(time, is_admin)
	return render_to_response("manager/statistics/sys_daily_detail.html", {'daily_detail': daily_detail})


@login_required(login_url='/manager/login/')
def monthly_coupon_statistics(request):
	return render_to_response("manager/statistics/monthly_coupon_statistics.html")


@login_required(login_url='/manager/login/')
def monthly_statistics(request):
	request_type = request.GET.get('type')
	if request_type == "consumers":
		is_admin = False
	else:
		is_admin = True

	date_str = request.GET.get('date')
	if (date_str):
		try:
			time = datetime.datetime.strptime(date_str, "%Y-%m-%d")
		except ValueError:
			time = datetime.datetime.today()
	else:
		time = datetime.datetime.today()

	daily_statistics_set = get_daily_statistics_set(time, is_admin)
	return render_to_response("manager/statistics/sys_monthly_statistics.html",
							  {'daily_statistics_set': daily_statistics_set})


def ticket_consume_record(request):
	time = datetime.datetime.today()
	date_str = request.GET.get('date')
	if (date_str):
		try:
			time = datetime.datetime.strptime(date_str, "%Y-%m-%d")
		except ValueError:
			time = datetime.datetime.today()
	else:
		time = datetime.datetime.today()

	consumed_tickets=Ticket.get_consumed_ticket_by_date(time)
	return render_to_response("manager/statistics/ticket_consume_record.html", locals())


def forum_index(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False

	return render(request, "manager/forum/index.html", {'current_user': current_user, 'is_admin': is_admin})


@ratelimit(rate='1/0s')
def forum_new_topic(request):
	current_user = request.user
	if (current_user.username == "admin"):
		print('admin')
		is_admin = True
	else:
		is_admin = False

	get_object_or_404(Category.objects.visible(),
					  pk=1)

	if request.method == 'POST':
		imagelist = request.POST.get("imagelist", "")
		form = TopicForm(user=request.user, data=request.POST)
		cform = CommentForm(user=request.user, data=request.POST)

		if not request.is_limited and all([form.is_valid(), cform.is_valid()]):  #
			# wrap in transaction.atomic?
			topic = form.save(commit=False)
			topic.category_id = 1
			topic.save()
			cform.topic = topic
			comment = cform.save()
			if imagelist:
				for cmid in imagelist.split(","):
					try:
						cimage = CommentImages.objects.get(id=cmid)
						cimage.comment = comment
						cimage.save()
					except Exception as ex:
						print ex.args
			comment_posted(comment=comment, mentions=cform.mentions)
		return redirect('/manager/forum' + topic.get_absolute_url())

	else:
		form = TopicForm(user=request.user, initial={'category': 1, })
		cform = CommentForm()

		context = {
			'form': form,
			'cform': cform,
			'current_user': current_user,
			'is_admin': is_admin
		}

		return render(request, "manager/forum/newtopic.html", context)


def forum_topic_detail(request,pk,slug):
	topic = Topic.objects.get_public_or_404(pk, request.user)

	if topic.slug != slug:
		return HttpResponsePermanentRedirect(topic.get_absolute_url())

	utils2.topic_viewed(request=request, topic=topic)

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

	for comment in comments:
		imagelist = CommentImages.objects.filter(comment = comment)
		comment.imagelist = imagelist

	context = {
		'topic': topic,
		'comments': comments,
		'time': time.time()
	}

	return render(request, 'manager/forum/topic/detail.html', context)


def forum_topic_list(request):
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

	for topic in topics:
		try:
			comment = Comment.objects.for_topic(topic=topic).for_user(topic.user).order_by("date")[0]
			topic.comment = comment
		except Exception as ex:
			pass

	context = {
		'categories': categories,
		'topics': topics,
		'ctime': time.time()
	}

	return render(request, 'manager/forum/topic/active.html', context)



def forum_topic_delete(request,pk=None):
	if request.user.is_authenticated() and Group.objects.get(id=3) in request.user.groups.all():
		return render(request, 'forum/topic/nopermit.html', {})

	categories = Category.objects \
		.visible() \
		.parents()

	topics = Topic.objects \
		.global_() \
		.with_bookmarks(user=request.user) \
		.order_by('-is_globally_pinned', '-last_active') \
		.select_related('category')

	topics = yt_paginate(
		topics,
		per_page=config.topics_per_page,
		page_number=request.GET.get('page', 1)
	)

	for topic in topics:
		try:
			comment = Comment.objects.for_topic(topic=topic).for_user(topic.user).order_by("date")[0]
			topic.comment = comment
		except Exception as ex:
			pass

	context = {
		'categories': categories,
		'topics': topics,
		'ctime': time.time(),
		'deltopic':True
	}

	return render(request, 'manager/forum/topic/active.html', context)


def forum_topic_unread(request):
	if request.user.is_authenticated() and Group.objects.get(id=3) in request.user.groups.all():
		return render(request, 'forum/topic/nopermit.html', {})

	categories = Category.objects \
		.visible() \
		.parents()

	readedtopiclist = TopicRead.objects.filter(user=request.user).values_list("topic",flat=True)
	print readedtopiclist

	topics = Topic.objects \
		.visible() \
		.global_() \
		.with_bookmarks(user=request.user) \
		.order_by('-is_globally_pinned', '-last_active') \
		.select_related('category')\
		.exclude(id__in=readedtopiclist)

	topics = yt_paginate(
		topics,
		per_page=config.topics_per_page,
		page_number=request.GET.get('page', 1)
	)

	for topic in topics:
		try:
			comment = Comment.objects.for_topic(topic=topic).for_user(topic.user).order_by("date")[0]
			topic.comment = comment
		except Exception as ex:
			pass

	context = {
		'categories': categories,
		'topics': topics,
		'ctime': time.time(),
		'unread':True
	}

	return render(request, 'manager/forum/topic/active.html', context)


def forum_slider_man(request):
	pass


@login_required
@ratelimit(rate='1/0s')
def forum_comment_publish(request, topic_id, pk=None):
	topic = get_object_or_404(
		Topic.objects.opened().for_access(request.user),
		pk=topic_id
	)

	if request.method == 'POST':
		imagelist = request.POST.get("imagelist","")
		form = CommentForm(user=request.user, topic=topic, data=request.POST)

		if not request.is_limited and form.is_valid():
			comment = form.save()
			if imagelist:
				for cmid in imagelist.split(","):
					try:
						cimage = CommentImages.objects.get(id=cmid)
						cimage.comment = comment
						cimage.save()
					except Exception as ex:
						print ex.args
			comment_posted(comment=comment, mentions=form.mentions)
			return redirect(request.POST.get('next', "/manager/forum"+comment.get_absolute_url()))
	else:
		initial = None

		if pk:
			comment = get_object_or_404(Comment.objects.for_access(user=request.user), pk=pk)
			quote = markdown.quotify(comment.comment, comment.user.username)
			initial = {'comment': quote, }

		form = CommentForm(initial=initial)

	context = {
		'form': form,
		'topic': topic
	}

	return render(request, 'forum/comment/publish.html', context)


def forum_comment_find(request,pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment_number = Comment.objects.filter(topic=comment.topic, date__lte=comment.date).count()
	url = paginator.get_url(comment.topic.get_absolute_url(),
							comment_number,
							config.comments_per_page,
							'page')
	return redirect("/manager/forum"+url)


@moderator_required
def forum_comment_delete(request, pk, remove=True):
	comment = get_object_or_404(Comment, pk=pk)

	if request.method == 'POST':
		Comment.objects\
			.filter(pk=pk)\
			.update(is_removed=remove)

		return redirect("/manager/forum"+comment.get_absolute_url())

	if remove:
		type2 = 'delete'
	else:
		type2 = 'undelete'

	context = {'comment': comment, 'type':type2}

	return render(request, 'manager/forum/comment/moderate.html', context)
