# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.conf import settings
import django.utils.timezone as timezone
import json


AJAX_REQUEST_URL = 'http://127.0.0.1:8000/weixin/view_ajax_request/?openid=OPENID&action=ACTION'
GETED_BONUS_URL = 'http://127.0.0.1:8000/weixin/view_geted_bonus/?id_record=ID_RECORD'
AGAIN_GET_BONUS_URL ='http://127.0.0.1:8000/weixin/view_again_rcv_bonus/?openid=OPENID'
CREATE_COMMON_BONUS_URL = 'http://127.0.0.1:8000/weixin/view_again_rcv_bonus/?openid=OPENID'
CREATE_RANDOM_BONUS_URL = 'http://127.0.0.1:8000/weixin/view_again_rcv_bonus/?openid=OPENID'

AJAX_GET_BONUS = 'ajax_get_bonus'


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
	base_type = 'get_bonus'
	static_url = settings.STATIC_URL
	openid = 'koovox'
	ajax_request_url = AJAX_REQUEST_URL.replace('OPENID', openid)
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
	ajax_request_url = AJAX_REQUEST_URL.replace('OPENID', openid)
	geted_bonus_url = GETED_BONUS_URL
	again_get_bonus_url = AGAIN_GET_BONUS_URL.replace('OPENID', openid)
	return render_to_response('get_bonus.html', locals())
	
#发红包界面认证
@csrf_exempt
def view_redirect_bonus_snd(request):
	#获取openid
	#刷新页面中openid
	title = '选择红包类型'
	base_type = 'bonus_type'
	static_url = settings.STATIC_URL
	openid = 'koovox'
	my_rcv_bonus_url = ''
	my_snd_bonus_url = ''
	my_bonus_range_url = ''
	create_common_bonus_url = CREATE_COMMON_BONUS_URL.replace('OPENID', openid)
	create_random_bonus_url = CREATE_RANDOM_BONUS_URL.replace('OPENID', openid)
	return render_to_response('bonus_type.html', locals())

#发普通红包
def view_common_bonus(request):
	#从request中解析出openid
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
	
class GetedBonus():
	def __init__(self, id_bonus, openid, name, picture, message, datetime, content):
		self.id_bonus = id_bonus
		self.openid = openid
		self.name = name
		self.picture = picture
		self.message = message
		self.datetime = datetime
		self.content = content
		
	
	
#抢到的红包界面
@csrf_exempt
def view_geted_bonus(request):
	id_record = request.GET.get('id_record')
	print("===view_geted_bonus:%s===\n"%(id_record))
	title = '东启湘厨'
	base_type = 'geted_bonus'
	static_url = settings.STATIC_URL
	bonus_dir1 = {"串串":"3串", "可乐":"2瓶", "甜品":"3个"}
	bonus_dir2 = {"串串":"6串", "可乐":"4瓶", "甜品":"7个"}
	bonus_dir3 = {"串串":"10串", "可乐":"2瓶", "甜品":"8个"}
	picture1 = 'http://wx.qlogo.cn/mmopen/9T7GtDDMnzaBB0ILSKYVrq1esXAVR4VKtiaYwhxOaFb7VJpgtsrsngBZRiavDsVvMibOnSxfDsZ4zGgbN6NlxB4CTIshrGAOvQD/0'
	picture2 = ' http://wx.qlogo.cn/mmopen/ZMdxSDafpxR1pC2gQK7tKP7L2fM35ic9dOSG2eAe1icQ3cKoHA34cbWqhHHlv6fKNzFGmiaACiaqSUvQ30jLlxO9R8GQELocGjkib/0'
	curr_time = timezone.now
	random1 = GetedBonus(id_bonus='1234', openid="2345", name="stephen", picture=picture1, message="恭喜发财", datetime=curr_time, content=bonus_dir1)
	random2 = GetedBonus(id_bonus='1454', openid="6345", name="hero", picture=picture2, message="生日快乐", datetime=curr_time, content=bonus_dir2)
	common = GetedBonus(id_bonus='1904', openid="6225", name="stephen", picture=picture1, message="对面的女孩开过来", datetime=curr_time, content=bonus_dir3)
	random_bonus = []
	common_bonus = []
	random_bonus.append(random1)
	random_bonus.append(random2)
	common_bonus.append(common)
	common_bonus_url = 'http://127.0.0.1:8000/weixin/view_ajax_request/?openid=OPENID&action=ACTION'
	return render_to_response('geted_bonus.html', locals())
	
#网页ajax请求
@csrf_exempt
def view_ajax_request(request):
	if request.method == 'GET':
		openid = request.GET.get('openid')
		action = request.GET.get('action')
		print('***view_ajax_request id:%s action:%s****\n'%(openid, action))
	else:
		print('***view_ajax_request body:%s ****\n'%(request.body))
		
		data = json.loads(request.body)
		for key, value in data.items():
			print('%s ==> %s'%(key, value))
	
	
	#实现ajax请求处理函数
	#response = handle_ajax_request(openid, action)
	response = '{"number":3, "id_record":"12345"}'
	return HttpResponse(response)

#微信token认证
@csrf_exempt
def view_token(request):
	pass


