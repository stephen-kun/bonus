# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.conf import settings
from weixin.models import DiningTable,Consumer,VirtualMoney, WalletMoney
from weixin.models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus
from topic.models import SliderImage, Topic
from comment.models import CommentImages, Comment
import random, string, json, pytz
import datetime

ADDRESS_IP = 'wx.tonki.com.cn'
VIEWS_FORUM_URL = 'http://%s/qubaba/get_forums'%(ADDRESS_IP)
VIEWS_SLIDEIMAGES_URL = 'http://%s/qubaba/get_slideimages'%(ADDRESS_IP)
VIEWS_BONUS_REMAIN_URL = 'http://%s/qubaba/bonus_remain'%(ADDRESS_IP)
VIEWS_BONUS_LIST_URL = 'http://%s/qubaba/qubaba_bonus_list'%(ADDRESS_IP)
VIEWS_PROMPT_BONUS_URL = 'http://%s/qubaba/prompt_bonus'%(ADDRESS_IP)
AJAX_HAS_BONUS_URL = 'http://%s/qubaba/has_bonus'%(ADDRESS_IP)
AJAX_BONUS_REMAIN_URL = 'http://%s/qubaba/ajax_bonus_remain'%(ADDRESS_IP)


class _QubabaForum():
	def __init__(self, topic):
		comments = Comment.objects.for_topic(topic=topic).order_by('date')
		self.comment = comments[0].comment
		imagelist = CommentImages.objects.filter(comment = comments[0])
		if imagelist:
			self.image = "http://%s/"%(ADDRESS_IP) + imagelist[0].imageurl
			self.has_image = 1
		else:
			self.has_image = 0		
		self.date_time = topic.date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Shanghai")).strftime('%m-%d %H:%M')
		consumer = Consumer.objects.filter(user=topic.user)[0]
		self.name = consumer.name
		self.picture = consumer.picture
		
# Create your views here.
#*****************大堂显示views************************
@csrf_exempt
def prompt_bonus(request):
	title = '抢串串'
	static_url = settings.STATIC_URL
	views_bonus_remain_url = VIEWS_BONUS_REMAIN_URL
	return render_to_response('prompt_bonus.html', locals())	

@csrf_exempt
def get_slideimages(request):
	title = '推荐菜品'
	static_url = settings.STATIC_URL	
	image_list = SliderImage.objects.filter(enabled=True)
	for image in image_list:
		image.url = "http://%s/media/"%(ADDRESS_IP) + str(image.url)
	views_forum_url = VIEWS_FORUM_URL
	ajax_has_bonus_url = AJAX_HAS_BONUS_URL
	views_prompt_bonus_url = VIEWS_PROMPT_BONUS_URL
	return render_to_response('slide_images.html', locals())	
	
@csrf_exempt
def get_forums(request):
	title = '龙门阵'
	static_url = settings.STATIC_URL	
	topics_len = Topic.objects.filter(is_removed=False).order_by('-is_globally_pinned', '-is_pinned', '-last_active').count()
	if topics_len > 10:
		topic_list = Topic.objects.filter(is_removed=False).order_by('-is_globally_pinned', '-is_pinned', '-last_active')[0:10]
	else:
		topic_list = Topic.objects.filter(is_removed=False).order_by('-is_globally_pinned', '-is_pinned', '-last_active')
	topics = []
	for topic in topic_list:
		qubaba_topic = _QubabaForum(topic)
		topics.append(qubaba_topic)
	views_slideimages_url = VIEWS_SLIDEIMAGES_URL
	ajax_has_bonus_url = AJAX_HAS_BONUS_URL
	views_prompt_bonus_url = VIEWS_PROMPT_BONUS_URL	
	return render_to_response('qubaba_forum.html', locals())	
		
@csrf_exempt
def has_bonus(request):
	data = {}
	snd_bonus_list = SndBonus.objects.filter(is_valid=True, is_exhausted=False)
	has_geted = 0
	if snd_bonus_list:
		data['has_bonus'] = 1
	else:
		data['has_bonus'] = 0	
	for snd_bonus in snd_bonus_list:
		if snd_bonus.bonus_exhausted:
			has_geted = 1
			break
	data['has_geted'] = has_geted
	data['state'] = 0
	return HttpResponse(json.dumps(data), content_type="application/json")

	
@csrf_exempt
def bonus_remain(request):
	title = '剩余串串'
	static_url = settings.STATIC_URL	
	length = SndBonus.objects.filter(is_valid=True, is_exhausted=False).count()
	snd_bonus_list = SndBonus.objects.filter(is_valid=True, is_exhausted=False)
	snd_bonus = None
	if length:
		snd_bonus = snd_bonus_list[0]
		remain = 0
		for rcv_bonus in RcvBonus.objects.filter(snd_bonus=snd_bonus, is_receive=False):
			remain += rcv_bonus.number
		snd_bonus.bonus_remain = remain
		snd_bonus.total_money = (snd_bonus.number - remain)*100 / snd_bonus.number
	else:
		snd_bonus = SndBonus.objects.all()[0]
	ajax_bonus_remain_url = AJAX_BONUS_REMAIN_URL
	views_bonus_list_url = VIEWS_BONUS_LIST_URL		
	return render_to_response('bonus_remain.html', locals())	
	
@csrf_exempt
def ajax_bonus_remain(request):
	data = {}
	length = SndBonus.objects.filter(is_valid=True, is_exhausted=False).count()
	snd_bonus_list = SndBonus.objects.filter(is_valid=True, is_exhausted=False)
	if length:
		rand = random.randint(0, length-1)
		data['has_bonus'] = 1
		data['type'] = snd_bonus_list[rand].bonus_type
		data['table'] = snd_bonus_list[rand].to_table
		data['name'] = snd_bonus_list[rand].consumer.name
		data['picture'] = str(snd_bonus_list[rand].consumer.picture)
		data['number'] = snd_bonus_list[rand].number
		remain = 0
		for rcv_bonus in RcvBonus.objects.filter(snd_bonus=snd_bonus_list[rand], is_receive=False):
			remain += rcv_bonus.number
		data['remain'] = remain
	else:
		data['has_bonus'] = 0
	data['state'] = 0
	return HttpResponse(json.dumps(data), content_type="application/json")
	
@csrf_exempt
def qubaba_bonus_list(request):
	title = '串串封神榜'
	static_url = settings.STATIC_URL	
	bonus_range = 1		
	length = Consumer.objects.filter(user__groups__name='consumer').count()
	if length > 8:
		consumer_list = Consumer.objects.filter(user__groups__name='consumer').order_by("rcv_bonus_num").reverse()[0:7]
	else:
		consumer_list = Consumer.objects.filter(user__groups__name='consumer').order_by("rcv_bonus_num").reverse()
		
	for consumer in consumer_list:
		consumer.bonus_range = bonus_range
		bonus_range += 1
	views_slideimages_url = VIEWS_SLIDEIMAGES_URL		
	ajax_has_bonus_url = AJAX_HAS_BONUS_URL
	views_prompt_bonus_url = VIEWS_PROMPT_BONUS_URL			
	return render_to_response('bonus_list.html', locals())	