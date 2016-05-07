# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist 
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.conf import settings
import django.utils.timezone as timezone
import json
from .wechat import PostResponse, wechat, TOKEN, APPID, APPSECRET
from .utils import  action_get_bonus, is_consumer_dining, handle_ajax_request, get_user_openid, decode_bonus_detail,create_bonus_dict
from .utils import check_geted_bonus, decode_choose_pay, get_bonus_type_str, get_record_openid, is_enough_pay, update_wallet_money
from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus


#ADDRESS_IP = '127.0.0.1:8000'
ADDRESS_IP = '120.76.122.53'

REDIRECT_RB_URL = 'http://%s/weixin/view_redirect_random_bonus'%(ADDRESS_IP)
REDIRECT_CB_URL = 'http://%s/weixin/view_redirect_common_bonus'%(ADDRESS_IP)
REDIRECT_SA_URL = 'http://%s/weixin/view_redirect_settle_account'%(ADDRESS_IP)
REDIRECT_UA_URL = 'http://%s/weixin/view_redirect_user_account'%(ADDRESS_IP)
REDIRECT_BS_URL = 'http://%s/weixin/view_redirect_bonus_snd'%(ADDRESS_IP)
REDIRECT_BR_URL = 'http://%s/weixin/view_redirect_bonus_rcv'%(ADDRESS_IP)
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URL&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)
AJAX_REQUEST_POST_URL = 'http://%s/weixin/view_ajax_request'%(ADDRESS_IP)
GETED_BONUS_URL = 'http://%s/weixin/view_geted_bonus'%(ADDRESS_IP)
GET_BONUS_URL ='http://%s/weixin/view_rcv_bonus'%(ADDRESS_IP)
SND_BONUS_URL ='http://%s/weixin/view_snd_bonus'%(ADDRESS_IP)
CREATE_COMMON_BONUS_URL = 'http://%s/weixin/view_common_bonus'%(ADDRESS_IP)
CREATE_RANDOM_BONUS_URL = 'http://%s/weixin/view_random_bonus'%(ADDRESS_IP)
SELF_RCV_BONUS_URL = 'http://%s/weixin/view_self_rcv_bonus'%(ADDRESS_IP)
SELF_SND_BONUS_URL = 'http://%s/weixin/view_self_snd_bonus'%(ADDRESS_IP)
SELF_BONUS_LIST_URL = 'http://%s/weixin/view_self_bonus_list'%(ADDRESS_IP)
CHOOSE_PAY_URL = 'http://%s/weixin/view_choose_pay'%(ADDRESS_IP)
SEND_MESSAGE_URL = 'http://%s/weixin/view_choose_pay'%(ADDRESS_IP)
BONUS_REFUSE_URL = 'http://%s/weixin/view_choose_pay'%(ADDRESS_IP)
USER_ACCOUNT_URL = 'http://%s/weixin/view_user_account'%(ADDRESS_IP)
USER_INFO_URL = 'http://%s/weixin/view_user_info'%(ADDRESS_IP)
USER_TICKET_URL = 'http://%s/weixin/view_user_ticket'%(ADDRESS_IP)
SETTLE_ACCOUNTS_URL = 'http://%s/weixin/view_settle_account'%(ADDRESS_IP)
BONUS_DETAIL_URL = 'http://%s/weixin/view_bonus_detail'%(ADDRESS_IP)


class _MenuUrl():
	get_bonus_url = GET_BONUS_URL
	snd_bonus_url = SND_BONUS_URL
	settle_accounts_url = SETTLE_ACCOUNTS_URL
	forum_url = ''
	user_account_url = USER_ACCOUNT_URL
	user_info_url = USER_INFO_URL
	user_ticket_url = USER_TICKET_URL
	self_bonus_list_url = SELF_BONUS_LIST_URL
	self_snd_bonus_url = SELF_SND_BONUS_URL
	self_rcv_bonus_url = SELF_RCV_BONUS_URL
	
	
# Create your views here.

def check_session_openid(request, redirect_uri, redirect_func):
	#openid = 'oJvvJwrakNQy8hA6CKLD5OcbQMH4'
	#return redirect_func(openid, request)
	if 'openid' in request.session:
		openid = request.session['openid']
		return redirect_func(openid, request)
	else:
		url = OAUTH_URL.replace('REDIRECT_URL', redirect_uri)
		return HttpResponseRedirect(url)

		
def display_prompt_views(message):
	title = '提示'
	static_url = settings.STATIC_URL
	prompt_message = message
	menu = _MenuUrl()
	return render_to_response("user_prompt.html", locals())		

def display_rcv_bonus_views(openid, request):
	#检测用户是否在用餐状态
	if is_consumer_dining(openid):
		title = '抢红包'
		static_url = settings.STATIC_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		geted_bonus_url = GETED_BONUS_URL
		openid = openid
		get_bonus_url = GET_BONUS_URL
		menu = _MenuUrl()
		return render_to_response('get_bonus.html', locals())
	else:
		prompt_message = '就餐用户独享抢红包！'
		return display_prompt_views(prompt_message)
		
def display_snd_bonus_views(openid, request):
	if is_consumer_dining(openid):	
		title = '选择红包类型'
		static_url = settings.STATIC_URL
		self_rcv_bonus_url = SELF_RCV_BONUS_URL
		self_snd_bonus_url = SELF_SND_BONUS_URL
		self_bonus_list_url = SELF_BONUS_LIST_URL
		create_common_bonus_url = CREATE_COMMON_BONUS_URL
		create_random_bonus_url = CREATE_RANDOM_BONUS_URL
		menu = _MenuUrl()		
		return render_to_response('bonus_type.html', locals())
	else:
		prompt_message = '就餐用户独享抢红包！'
		return display_prompt_views(prompt_message)	

def display_settle_account_views(openid, request):	
	if is_consumer_dining(openid):		
		title = '结算'
		static_url = settings.STATIC_URL
		consumer = Consumer.objects.get(open_id=openid)
		total_money = consumer.session.total_money
		update_wallet_money(consumer)
		wallet_money = consumer.own_bonus_value
		ajax_request_url = AJAX_REQUEST_POST_URL
		menu = _MenuUrl()
		return render_to_response('close_an_account.html', locals())		
	else:
		prompt_message = '就餐用户独享抢红包！'
		return display_prompt_views(prompt_message)		

def display_user_account_views(openid, request):
	title = '我'
	static_url = settings.STATIC_URL	
	consumer = Consumer.objects.get(open_id=openid)
	good_list = decode_bonus_detail(consumer)
	user_ticket_url = USER_TICKET_URL
	user_info_url = USER_INFO_URL
	menu = _MenuUrl()
	return render_to_response('user_account.html', locals())	
	
#个人信息
@csrf_exempt
def view_user_info(request):
	pass

#个人礼券
@csrf_exempt
def view_user_ticket(request):
	pass

#发红包界面	
@csrf_exempt
def view_snd_bonus(request):
	print('---**view_snd_bonus**---\n')
	return check_session_openid(request, REDIRECT_BS_URL, display_snd_bonus_views)	
		
#抢红包界面
@csrf_exempt
def view_rcv_bonus(request):
	print('---**view_rcv_bonus**---\n')
	return check_session_openid(request, REDIRECT_BR_URL, display_rcv_bonus_views)
	
#结算界面
@csrf_exempt
def view_settle_account(request):	
	print('---**view_settle_account**---\n')
	return check_session_openid(request, REDIRECT_SA_URL, display_settle_account_views)
	
#我的个人界面
@csrf_exempt
def view_user_account(request):	
	print('---**view_user_account**---\n')
	return check_session_openid(request, REDIRECT_UA_URL, display_user_account_views)
	
#结算界面认证
@csrf_exempt
def view_redirect_settle_account(request):	
	print('---view_redirect_settle_account---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_settle_account_views(openid, request)		
	
#我的个人界面认证
@csrf_exempt
def view_redirect_user_account(request):	
	print('---view_redirect_user_account---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_user_account_views(openid, request)


#发红包界面认证	
@csrf_exempt
def view_redirect_bonus_snd(request): 
	print('---view_redirect_bonus_snd---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_snd_bonus_views(openid, request)
	
	
#抢红包界面认证
@csrf_exempt
def view_redirect_bonus_rcv(request):
	print('---view_redirect_bonus_rcv---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_rcv_bonus_views(openid, request)
	
def display_common_bonus_views(open_id, request):
	title = '普通红包'
	static_url = settings.STATIC_URL
	good_list = create_bonus_dict(request)
	choose_pay_url = CHOOSE_PAY_URL
	openid = open_id
	menu = _MenuUrl()
	return render_to_response('common_bonus.html', locals())	
	
@csrf_exempt
def view_redirect_common_bonus(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_common_bonus_views(openid, request)
		
#发普通红包
@csrf_exempt
def view_common_bonus(request):
	#从request中解析出openid
	print("========view_common_bonus =========\n")
	return check_session_openid(request, REDIRECT_CB_URL, display_common_bonus_views)
	
def display_random_bonus_views(open_id, request):
	title = '手气红包'
	static_url = settings.STATIC_URL	
	good_list = create_bonus_dict(request)
	choose_pay_url = CHOOSE_PAY_URL
	openid = open_id
	menu = _MenuUrl()
	return render_to_response('random_bonus.html', locals())	

@csrf_exempt
def view_redirect_random_bonus(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_random_bonus_views(openid, request)	
	
#发手气红包
@csrf_exempt
def view_random_bonus(request):
	print("========view_random_bonus =========\n")
	return check_session_openid(request, REDIRECT_RB_URL, display_random_bonus_views)
	
#串串详情
@csrf_exempt
def view_bonus_detail(request):
	print("========view_bonus_detail =========\n")
	title = '串串明细'
	openid = request.session['openid']	
	static_url = settings.STATIC_URL	
	return render_to_response('bonus_detail_info.html', locals())
	
def display_self_rcv_bonus(open_id, request):
	title = '收到的串串'
	openid = open_id
	static_url = settings.STATIC_URL
	consumer = Consumer.objects.get(open_id=openid)
	rcv_bonus_list = RcvBonus.objects.filter(consumer=consumer).order_by("datetime").reverse()
	bonus_detail_url = BONUS_DETAIL_URL
	menu = _MenuUrl()	
	return render_to_response('self_rcv_bonus.html', locals())	

@csrf_exempt	
def view_redirect_self_rcv_bonus(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_self_rcv_bonus(openid, request)		
	
#check收到的串串
@csrf_exempt
def view_self_rcv_bonus(request):
	print("========view_self_rcv_bonus =========\n")	
	return check_session_openid(request, REDIRECT_RB_URL, display_self_rcv_bonus)

#check发出的串串
@csrf_exempt
def view_self_snd_bonus(request):
	#获取openid
	print("========view_self_rcv_bonus =========\n")	
	title = '发出的串串'
	openid = request.session['openid']
	static_url = settings.STATIC_URL
	consumer = Consumer.objects.get(open_id=openid)
	snd_bonus_list = SndBonus.objects.filter(consumer=consumer).order_by("create_time").reverse()
	bonus_detail_url = BONUS_DETAIL_URL
	menu = _MenuUrl()
	return render_to_response('self_snd_bonus.html', locals())
	
#check串串排行榜
@csrf_exempt
def view_self_bonus_list(request):
	openid = request.session['openid']
	print("========view_self_bonus_list :%s=========\n"%(openid))	
	title = '串串排行榜'
	static_url = settings.STATIC_URL
	try:
		bonus_range = 1
		consumer_list = Consumer.objects.all().order_by("rcv_bonus_num").reverse()
		for consumer in consumer_list:
			consumer.bonus_range = bonus_range
			bonus_range += 1
			consumer.save()
		oneself = Consumer.objects.get(open_id=openid)
		top_consumer = consumer_list[0]
		menu = _MenuUrl()
		return render_to_response('self_bonus_list.html', locals())
	except ObjectDoesNotExist:
		return HttpResponseBadRequest("Invalid param!")
		
#网页ajax请求
@csrf_exempt
def view_ajax_request(request):	
	print('***view_ajax_request body: ****\n')
	data = json.loads(request.body)
	session = request.session
	action = data['action']
	for key, value in data.items():
		print('%s ==> %s'%(key, value))
		
	#实现ajax请求处理函数
	response = handle_ajax_request(action, data, session)

	return HttpResponse(response)
	
#抢到的红包界面
@csrf_exempt
def view_geted_bonus(request):
	if "id_record" in request.session:
		id_record = request.session['id_record']
		print("===view_geted_bonus:%s===\n"%(id_record))
		title = '抢到的红包'
		static_url = settings.STATIC_URL
		bonus_dir = check_geted_bonus(id_record)
		openid = get_record_openid(id_record)
		random_bonus = bonus_dir['random_bonus']
		common_bonus = bonus_dir['common_bonus']
		system_bonus = bonus_dir['system_bonus']	
		common_bonus_url = CREATE_COMMON_BONUS_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		del request.session['id_record']
		menu = _MenuUrl()
		return render_to_response('geted_bonus.html', locals())
	else:
		return check_session_openid(request, REDIRECT_BR_URL, display_rcv_bonus_views)

#支付页面
@csrf_exempt	
def view_choose_pay(request):
	print("+++view_choose_pay +++\n")
	for key ,value in request.GET.items():
		print("%s ==> %s"%(key, value))
		
	openid = request.GET.get('openid')	
	if 'openid' in request.session == False:
		request.session['openid'] = openid
	consumer = Consumer.objects.get(open_id=openid)
	title = '支付'
	body_class = 'qubaba_hsbj'
	static_url = settings.STATIC_URL
	result_dir = decode_choose_pay(request, request.GET)
	good_list = result_dir['good_list']
	total_money = result_dir['total_money']
	enough_money = is_enough_pay(consumer, request.GET)
	ajax_request_url = AJAX_REQUEST_POST_URL
	menu = _MenuUrl()
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

