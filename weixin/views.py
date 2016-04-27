# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.conf import settings
import django.utils.timezone as timezone
import json
from .wechat import PostResponse, wechat, TOKEN, APPID, APPSECRET
from .utils import  action_get_bonus, is_consumer_dining, handle_ajax_request, get_user_openid, decode_bonus_detail,create_bonus_dir

from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import Dining,Ticket, RcvBonus, BonusMessage,SndBonus,Recharge, RecordRcvBonus


REDIRECT_SA_URL = 'http://120.76.122.53/weixin/view_redirect_settle_account'
REDIRECT_UA_URL = 'http://120.76.122.53/weixin/view_redirect_user_account'
REDIRECT_BS_URL = 'http://120.76.122.53/weixin/view_redirect_bonus_snd'
REDIRECT_BR_URL = 'http://120.76.122.53/weixin/view_redirect_bonus_rcv'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URL&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)
AJAX_REQUEST_GET_URL = 'http://120.76.122.53/weixin/view_ajax_request/?openid=OPENID&action=ACTION'
AJAX_REQUEST_POST_URL = 'http://120.76.122.53/weixin/view_ajax_request'
GETED_BONUS_URL = 'http://120.76.122.53/weixin/view_geted_bonus/?id_record=ID_RECORD'
AGAIN_GET_BONUS_URL ='http://120.76.122.53/weixin/view_again_rcv_bonus/?openid=OPENID'
CREATE_COMMON_BONUS_URL = 'http://120.76.122.53/weixin/view_common_bonus/?openid=OPENID'
CREATE_RANDOM_BONUS_URL = 'http://120.76.122.53/weixin/view_random_bonus/?openid=OPENID'
SELF_RCV_BONUS_URL = 'http://120.76.122.53/weixin/view_self_rcv_bonus/?openid=OPENID'
SELF_SND_BONUS_URL = 'http://120.76.122.53/weixin/view_self_snd_bonus/?openid=OPENID'
SELF_BONUS_LIST_URL = 'http://120.76.122.53/weixin/view_self_bonus_list/?openid=OPENID'
CHOOSE_PAY_URL = 'http://120.76.122.53/weixin/view_choose_pay/?openid=OPENID'



# Create your views here.

#发红包界面	
@csrf_exempt
def view_snd_bonus(request):
	print('---**view_snd_bonus**---\n')
	url = OAUTH_URL.replace('REDIRECT_URL', REDIRECT_BS_URL)
	return HttpResponseRedirect(url)	
	
#抢红包界面
@csrf_exempt
def view_rcv_bonus(request):
	print('---**view_rcv_bonus**---\n')
	url = OAUTH_URL.replace('REDIRECT_URL', REDIRECT_BR_URL)
	return HttpResponseRedirect(url)
	
#结算界面
@csrf_exempt
def view_settle_account(request):	
	print('---**view_settle_account**---\n')
	url = OAUTH_URL.replace('REDIRECT_URL', REDIRECT_SA_URL)
	return HttpResponseRedirect(url)
	
#我的个人界面
@csrf_exempt
def view_user_account(request):	
	print('---**view_user_account**---\n')
	url = OAUTH_URL.replace('REDIRECT_URL', REDIRECT_UA_URL)
	return HttpResponseRedirect(url)
	
#结算界面认证
@csrf_exempt
def view_redirect_settle_account(request):	
	print('---view_redirect_settle_account---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	static_url = settings.STATIC_URL	
	if is_consumer_dining(openid):		
		title = '结算'
		body_class = 'qubaba_hsbj'	
		consumer = Consumer.objects.get(open_id=openid)
		total_money = consumer.on_table.total_money
		ajax_request_url = AJAX_REQUEST_POST_URL
		return render_to_response('close_an_account.html', locals())		
	else:
		title = '提示'
		article_class = 'issue-bj stanson'
		prompt_message = '就餐用户独享抢红包！'
		return render_to_response("user_prompt.html", locals())			
	
#我的个人界面认证
@csrf_exempt
def view_redirect_user_account(request):	
	print('---view_redirect_user_account---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	title = '我'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL	
	consumer = Consumer.objects.get(open_id=openid)
	good_list = decode_bonus_detail(consumer)
	user_ticket_url = ''
	user_info_url = ''
	return render_to_response('user_account.html', locals())

#发红包界面认证	
@csrf_exempt
def view_redirect_bonus_snd(request): 
	print('---view_redirect_bonus_snd---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	print('======openid:%s\n' %(openid))
	if is_consumer_dining(openid):	
		title = '选择红包类型'
		body_class = 'red_cen'
		static_url = settings.STATIC_URL
		self_rcv_bonus_url = SELF_RCV_BONUS_URL.replace('OPENID', openid)
		self_snd_bonus_url = SELF_SND_BONUS_URL.replace('OPENID', openid)
		self_bonus_list_url = SELF_BONUS_LIST_URL.replace('OPENID', openid)
		create_common_bonus_url = CREATE_COMMON_BONUS_URL.replace('OPENID', openid)
		create_random_bonus_url = CREATE_RANDOM_BONUS_URL.replace('OPENID', openid)
		return render_to_response('bonus_type.html', locals())
	else:
		title = '提示'
		article_class = 'issue-bj stanson'
		static_url = settings.STATIC_URL
		prompt_message = '就餐用户独享抢红包！'
		return render_to_response("user_prompt.html", locals())		
	
#继续抢红包界面
@csrf_exempt
def view_again_rcv_bonus(request):
	openid = request.GET.get('openid')
	print('**view_again_rcv_bonus:%s***'%(openid))
	title = '东启湘厨'
	body_class = 'red_q'
	static_url = settings.STATIC_URL
	ajax_request_url = AJAX_REQUEST_URL.replace('OPENID', openid)
	geted_bonus_url = GETED_BONUS_URL
	again_get_bonus_url = AGAIN_GET_BONUS_URL.replace('OPENID', openid)
	return render_to_response('get_bonus.html', locals())
	
#抢红包界面认证
@csrf_exempt
def view_redirect_bonus_rcv(request):
	#获取openid
	#刷新页面中openid
	print('---view_redirect_bonus_rcv---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	#检测用户是否在用餐状态
	if is_consumer_dining(openid):
		title = '东启湘厨'
		body_class = 'red_q'
		static_url = settings.STATIC_URL
		ajax_request_url = AJAX_REQUEST_URL.replace('OPENID', openid)
		geted_bonus_url = GETED_BONUS_URL
		again_get_bonus_url = AGAIN_GET_BONUS_URL.replace('OPENID', openid)
		return render_to_response('get_bonus.html', locals())
	else:
		title = '提示'
		article_class = 'issue-bj stanson'
		static_url = settings.STATIC_URL
		prompt_message = '就餐用户独享抢红包！'
		return render_to_response("user_prompt.html", locals())	
		
#发普通红包
@csrf_exempt
def view_common_bonus(request):
	#从request中解析出openid
	openid = request.GET.get('openid')
	print("========view_common_bonus :%s=========\n"%(openid))
	title = '普通红包'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL
	good_list = create_bonus_dir()
	choose_pay_url = CHOOSE_PAY_URL.replace("OPENID", openid)
	return render_to_response('common_bonus.html', locals())
	
#发手气红包
def view_random_bonus(request):
	#从request中解析出openid
	openid = request.GET.get('openid')
	print("========view_random_bonus :%s=========\n"%(openid))
	title = '手气红包'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL	
	good_list = create_bonus_dir()
	choose_pay_url = CHOOSE_PAY_URL.replace("OPENID", openid)
	return render_to_response('random_bonus.html', locals())
	
#check收到的串串
@csrf_exempt
def view_self_rcv_bonus(request):
	#获取openid
	openid = request.GET.get('openid')
	print("========view_self_rcv_bonus :%s=========\n"%(openid))	
	title = '收到的串串'
	article_class = 'issue-bj'
	static_url = settings.STATIC_URL
	picture = 'http://wx.qlogo.cn/mmopen/9T7GtDDMnzaBB0ILSKYVrq1esXAVR4VKtiaYwhxOaFb7VJpgtsrsngBZRiavDsVvMibOnSxfDsZ4zGgbN6NlxB4CTIshrGAOvQD/0'
	table = DiningTable.objects.get(index_table='1')
	consumer_tuple = Consumer.objects.get_or_create(open_id=openid, name="stephen", picture=picture, on_table=table)
	consumer = consumer_tuple[0]
	rcv_bonus = RcvBonus.objects.filter(consumer=consumer).order_by("datetime").reverse()
	return render_to_response('self_rcv_bonus.html', locals())

#check发出的串串
@csrf_exempt
def view_self_snd_bonus(request):
	#获取openid
	openid = request.GET.get('openid')
	print("========view_self_rcv_bonus :%s=========\n"%(openid))	
	title = '收到的串串'
	article_class = 'issue-bj stanson'
	static_url = settings.STATIC_URL
	consumer = Consumer.objects.get(open_id=openid)
	rcv_bonus = SndBonus.objects.filter(consumer=consumer).order_by("create_time").reverse()
	return render_to_response('self_snd_bonus.html', locals())
	
#check串串排行榜
@csrf_exempt
def view_self_bonus_list(request):
	openid = request.GET.get('openid')
	print("========view_self_bonus_list :%s=========\n"%(openid))	
	title = '收到的串串'
	article_class = 'issue-bj stanson'
	static_url = settings.STATIC_URL
	oneself = Consumer.objects.get(open_id=openid)
	consumer_list = Consumer.objects.all().order_by("bonus_range").reverse()	
	top_consumer = consumer_list[0]
	return render_to_response('self_bonus_list.html', locals())
		
#网页ajax请求
@csrf_exempt
def view_ajax_request(request):
	if request.method == 'GET':
		openid = request.GET.get('openid')
		action = request.GET.get('action')
		data = None
		print('***view_ajax_request id:%s action:%s****\n'%(openid, action))
	else:
		print('***view_ajax_request body:%s ****\n'%(request.body))
		data = json.loads(request.body)
		openid = data['openid']
		action = data['action']
		for key, value in data.items():
			print('%s ==> %s'%(key, value))
		
	#实现ajax请求处理函数
	response = handle_ajax_request(openid, action, data)

	return HttpResponse(response)

#抢到的红包界面
@csrf_exempt
def view_geted_bonus(request):
	id_record = request.GET.get('id_record')
	print("===view_geted_bonus:%s===\n"%(id_record))
	title = '东启湘厨'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL
	
	common_bonus_url = CREATE_COMMON_BONUS_URL.replace('OPENID', id_record)
	return render_to_response('geted_bonus.html', locals())

#支付页面
@csrf_exempt	
def view_choose_pay(request):
	openid = request.GET.get('openid')
	print("+++view_choose_pay %s+++\n"%(openid))
	consumer = Consumer.objects.get(open_id=openid)
	title = '东启湘厨'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL	
	total_money = 105
	enough_money = False
	return render_to_response('weixin_pay.html', locals())
    
@csrf_exempt
def view_wechat_token(request):
	if request.method == 'GET':
		# 检验合法性
		# 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
		signature = request.GET.get('signature')
		timestamp = request.GET.get('timestamp')
		nonce = request.GET.get('nonce')

		if not wechat.check_signature(signature, timestamp, nonce):
			return HttpResponseBadRequest('Verify Failed')

		return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")  
	
	response = PostResponse(request)
	return response.auto_handle()

