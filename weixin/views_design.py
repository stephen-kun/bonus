# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.conf import settings


ACTION_GET_BONUS_URL = 'http://127.0.0.1:8000/weixin/view_action_get_bonus/?openid=OPENID'
GETED_BONUS_URL = 'http://127.0.0.1:8000/weixin/view_geted_bonus'
AGAIN_GET_BONUS_URL ='http://127.0.0.1:8000/weixin/view_again_rcv_bonus/?openid=OPENID'

# Create your views here.

#我的钱包界面
def view_my_wallet(request):
	pass
	
#我的钱包界面认证
def view_redirect_my_wallet(request):
	#获取openid
	#根据openid查询Consumer表中own_bonus_value，own_bonus_detail，own_ticket_value，刷新页面信息		
	pass 
	
#结算界面
def view_settle_account(request):	
	pass
	
#结算界面认证
def view_redirect_settle_account(request):
	#获取openid
	#刷新页面中openid	
	pass

#发红包界面
@csrf_exempt
def view_snd_bonus(request):
	pass
	
#抢红包界面
@csrf_exempt
def view_rcv_bonus(request):
	pass
	
#抢红包界面认证
@csrf_exempt
def view_redirect_bonus_rcv(request):
	#获取openid
	#刷新页面中openid
	title = '东启湘厨'
	static_url = settings.STATIC_URL
	openid = 'koovox'
	action_get_bonus_url = ACTION_GET_BONUS_URL.replace('OPENID', openid)
	geted_bonus_url = GETED_BONUS_URL
	again_get_bonus_url = AGAIN_GET_BONUS_URL.replace('OPENID', openid)
	return render_to_response('get_bonus.html', locals())

	
#继续抢红包界面
@csrf_exempt
def view_again_rcv_bonus(request):
	openid = request.GET.get('openid')
	print('**view_again_rcv_bonus:%s***'%(openid))
	title = '东启湘厨'
	base_type = 'get_bonus'
	static_url = settings.STATIC_URL
	action_get_bonus_url = ACTION_GET_BONUS_URL.replace('OPENID', openid)
	geted_bonus_url = GETED_BONUS_URL
	again_get_bonus_url = AGAIN_GET_BONUS_URL.replace('OPENID', openid)
	return render_to_response('get_bonus.html', locals())
	
#发红包界面认证
@csrf_exempt
def view_redirect_bonus_snd(request):
	#获取openid
	#刷新页面中openid	
	pass

#发普通红包
def view_common_bonus(request):
	#从request中解析出openid以及tableid
	#刷新页面中的openid以及tableid
	pass
	
#发手气红包
def view_random_bonus(request):
	#从request中解析出openid以及tableid
	#刷新页面中的openid以及tableid	
	pass
	
#发系统红包
def view_system_bonus(request):
	#从request中解析出adminId
	#刷新页面中的adminId	
	pass
	
#抢红包动作
@csrf_exempt
def view_action_get_bonus(request):
	openid = request.GET.get('openid')
	print('***view_action_get_bonus :%s***\n'%(openid))
	#openid = request.body
	#response=action_get_bonus(openid)
	return HttpResponse('3')

#抢到的红包界面
@csrf_exempt
def view_geted_bonus(request):
	return HttpResponse('ok')

#微信token认证
@csrf_exempt
def view_token(request):
	pass


