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
from .utils import check_geted_bonus, decode_choose_pay, get_bonus_type_str, get_record_openid, is_enough_pay, update_wallet_money, log_print
from .models import DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus

from .wx_config import *




class _MenuUrl():
	get_bonus_url = GET_BONUS_URL
	snd_bonus_url = SND_BONUS_URL
	settle_accounts_url = SETTLE_ACCOUNTS_URL
	forum_url = QUBABA_FORUM_URL
	user_account_url = USER_ACCOUNT_URL
	user_info_url = USER_INFO_URL
	user_ticket_url = USER_TICKET_URL
	self_bonus_list_url = SELF_BONUS_LIST_URL
	self_snd_bonus_url = SELF_SND_BONUS_URL
	self_rcv_bonus_url = SELF_RCV_BONUS_URL
	
class _UserInfoUrl():
	name = 'http://%s/weixin/view_user_name'%(ADDRESS_IP)
	sex = 'http://%s/weixin/view_user_sex'%(ADDRESS_IP)
	phone = 'http://%s/weixin/view_user_phone'%(ADDRESS_IP)
	address = 'http://%s/weixin/view_user_address'%(ADDRESS_IP)
	email = 'http://%s/weixin/view_user_email'%(ADDRESS_IP)	
	
# Create your views here.

#*********************个人信息修改views*****************
@csrf_exempt
def view_user_phone(request):
	try:
		openid = request.session['openid']
		title = '修改电话'
		static_url = settings.STATIC_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		user_info_url = USER_INFO_URL
		return render_to_response("user_info_phone.html", locals())		
	except:
		log_print(view_user_phone)
		return HttpResponseBadRequest('error')
		
@csrf_exempt
def view_user_name(request):
	try:
		openid = request.session['openid']
		title = '修改昵称'
		static_url = settings.STATIC_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		user_info_url = USER_INFO_URL
		return render_to_response("user_info_name.html", locals())		
	except:
		log_print(view_user_name)
		return HttpResponseBadRequest('error')
		
@csrf_exempt
def view_user_address(request):
	try:
		openid = request.session['openid']
		title = '修改地址'
		static_url = settings.STATIC_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		user_info_url = USER_INFO_URL
		return render_to_response("user_info_address.html", locals())		
	except:
		log_print(view_user_address)
		return HttpResponseBadRequest('error')

@csrf_exempt
def view_user_email(request):
	try:
		openid = request.session['openid']
		title = '修改电话'
		static_url = settings.STATIC_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		user_info_url = USER_INFO_URL
		return render_to_response("user_info_email.html", locals())		
	except:
		log_print(view_user_email)
		return HttpResponseBadRequest('error')

@csrf_exempt
def view_user_sex(request):
	try:
		openid = request.session['openid']
		title = '修改性别'
		static_url = settings.STATIC_URL
		consumer = Consumer.objects.get(open_id=openid)
		ajax_request_url = AJAX_REQUEST_POST_URL
		user_info_url = USER_INFO_URL
		return render_to_response("user_info_sex.html", locals())		
	except:
		log_print(view_user_sex)
		return HttpResponseBadRequest('error')		


#*********************餐行健对接接口*****************

#验券接口
@csrf_exempt
def check_consumer_code(request):
	try:
		data_dict = json.loads(request.body)
		id_ticket = str(data_dict['ticket_code'])
		ticket = Ticket.objects.filter(id_ticket=id_ticket)
		ticket_value = float(0)
		response = {}
		if len(ticket) and (ticket[0].is_consume):
			response = dict(status=1, err_msg="该券已使用")
		elif len(ticket) and (ticket[0].is_consume == False):
			ticket_value = ticket[0].ticket_value
			ticket[0].is_consume = True
			ticket[0].save()
			response = dict(status=0, ticket_value=ticket_value)
		else:
			response = dict(status=2, err_msg="券码错误")
		return HttpResponse(response)
	except Exception as e:
		# 生成日志
		log_print(check_consumer_code)
		return HttpResponseBadRequest("Invalid param!")	

#请桌接口
@csrf_exempt
def release_dining_table(request):		
	try:
		data_dict = json.loads(request.body)
		index_table = str(data_dict['table'])
		table = DiningTable.objects.get(index_table=index_table)
		if table.status:
			consumer_list = Consumer.objects.filter(on_table=table)
			for consumer in consumer_list:
				consumer.on_table = None
				consumer.session = None
				consumer.save()
			table.status = False
			table.save()
		return HttpResponse('ok')	
	except Exception as e:
		# 生成日志
		log_print(release_dining_table)
		return HttpResponseBadRequest("Invalid param!")			

#**************微信入口界面必须做认证，不能用session*******************
@csrf_exempt
def view_redirect_func(redirect_uri):
	url = OAUTH_URL.replace('REDIRECT_URL', redirect_uri)
	return HttpResponseRedirect(url)
	
#我的个人界面
@csrf_exempt
def view_user_account(request):	
	#print('---**view_user_account**---\n')
	return view_redirect_func(REDIRECT_UA_URL)
	
#发红包界面	
@csrf_exempt
def view_snd_bonus(request):
	#print('---**view_snd_bonus**---\n')
	return view_redirect_func(REDIRECT_BS_URL)	
		
#抢红包界面
@csrf_exempt
def view_rcv_bonus(request):
	#print('---**view_rcv_bonus**---\n')
	return view_redirect_func(REDIRECT_BR_URL)	
	
#结算界面
@csrf_exempt
def view_settle_account(request):	
	#print('---**view_settle_account**---\n')
	return view_redirect_func(REDIRECT_SA_URL)
	
#论坛界面
@csrf_exempt
def view_qubaba_forum(request):
	return view_redirect_func(REDIRECT_QF_URL)
	
#论坛界面重定向
@csrf_exempt
def view_redirect_qubaba_forum(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_qubaba_forum_views(openid, request)	
	
def display_qubaba_forum_views(open_id, request):
	#url = 'http://www.jinfuture.com:9999/wx/?open_id=%s'%(open_id)
	url = 'http://wx.tonki.com.cn/wx/?open_id=%s'%(open_id)
	return HttpResponseRedirect(url)

#******************************************************************************	

def check_session_openid(request, redirect_uri, redirect_func):
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

def display_rcv_bonus_views(open_id, request):
	#检测用户是否在用餐状态
	openid = open_id
	if is_consumer_dining(openid):
		title = '抢红包'
		static_url = settings.STATIC_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		geted_bonus_url = GETED_BONUS_URL
		get_bonus_url = GET_BONUS_URL
		menu = _MenuUrl()
		return render_to_response('get_bonus.html', locals())
	else:
		prompt_message = '就餐用户独享抢红包！'
		return display_prompt_views(prompt_message)
		
def display_snd_bonus_views(open_id, request):
	openid = open_id
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

def display_settle_account_views(open_id, request):	
	openid = open_id
	try:
		if is_consumer_dining(openid):		
			title = '结算'
			static_url = settings.STATIC_URL
			consumer = Consumer.objects.get(open_id=openid)
			total_money = consumer.session.total_money
			consumer = update_wallet_money(consumer)
			wallet_money = consumer.own_bonus_value
			ajax_request_url = AJAX_REQUEST_POST_URL
			menu = _MenuUrl()
			return render_to_response('close_an_account.html', locals())		
		else:
			prompt_message = '就餐用户独享抢红包！'
			return display_prompt_views(prompt_message)	
	except:
		log_print(display_settle_account_views) 
		return HttpResponseBadRequest('Bad request')

def display_user_account_views(open_id, request):
	try:
		title = '我'
		openid = open_id
		static_url = settings.STATIC_URL	
		consumer = Consumer.objects.get(open_id=openid)
		consumer = update_wallet_money(consumer)
		good_list = decode_bonus_detail(consumer)
		user_ticket_url = USER_TICKET_URL
		user_info_url = USER_INFO_URL
		menu = _MenuUrl()
		return render_to_response('user_account.html', locals())	
	except:
		log_print(display_user_account_views) 
		return HttpResponseBadRequest('Bad request')	
	
def display_user_info(open_id, request):
	try:
		title = '个人信息'
		openid = open_id
		static_url = settings.STATIC_URL	
		consumer = Consumer.objects.get(open_id=openid)
		menu = _MenuUrl()
		user_info = _UserInfoUrl()
		return render_to_response('user_info.html', locals())			
	except:
		log_print(display_user_info) 
		return HttpResponseBadRequest('Bad request')			

@csrf_exempt
def view_redirect_user_info(request):
	#print('---view_redirect_user_info---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_user_info(openid, request)	
	
#个人信息
@csrf_exempt
def view_user_info(request):
	#print('---**view_user_info**---\n')
	return check_session_openid(request, REDIRECT_UI_URL, display_user_info)	
	
def display_user_ticket(open_id, request):
	try:
		title = '我的消费券'
		openid = open_id
		static_url = settings.STATIC_URL	
		consumer = Consumer.objects.get(open_id=openid)
		ticket_list = Ticket.objects.filter(consumer=consumer)
		menu = _MenuUrl()
		return render_to_response('user_ticket.html', locals())	
	except:
		log_print(display_user_ticket) 
		return HttpResponseBadRequest('Bad request')	
	
@csrf_exempt
def view_redirect_user_ticket(request):
	#print('---view_redirect_user_ticket---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_user_ticket(openid, request)		

#个人礼券
@csrf_exempt
def view_user_ticket(request):
	#print('---**view_user_ticket**---\n')
	return check_session_openid(request, REDIRECT_UT_URL, display_user_ticket)	
	
#结算界面认证
@csrf_exempt
def view_redirect_settle_account(request):	
	#print('---view_redirect_settle_account---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_settle_account_views(openid, request)		
	
#我的个人界面认证
@csrf_exempt
def view_redirect_user_account(request):	
	#print('---view_redirect_user_account---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_user_account_views(openid, request)


#发红包界面认证	
@csrf_exempt
def view_redirect_bonus_snd(request): 
	#print('---view_redirect_bonus_snd---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_snd_bonus_views(openid, request)
	
	
#抢红包界面认证
@csrf_exempt
def view_redirect_bonus_rcv(request):
	#print('---view_redirect_bonus_rcv---\n')
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_rcv_bonus_views(openid, request)
	
def display_common_bonus_views(open_id, request):
	try:
		title = '普通红包'
		static_url = settings.STATIC_URL
		good_list = create_bonus_dict(request)
		ajax_request_url = AJAX_REQUEST_POST_URL
		choose_pay_url = CHOOSE_PAY_URL
		openid = open_id
		menu = _MenuUrl()
		return render_to_response('common_bonus.html', locals())	
	except:
		log_print(display_common_bonus_views) 
		return HttpResponseBadRequest('Bad request')		
	
@csrf_exempt
def view_redirect_common_bonus(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_common_bonus_views(openid, request)
		
#发普通红包
@csrf_exempt
def view_common_bonus(request):
	#从request中解析出openid
	#print("========view_common_bonus =========\n")
	return check_session_openid(request, REDIRECT_CB_URL, display_common_bonus_views)
	
def display_random_bonus_views(open_id, request):
	try:
		title = '手气红包'
		static_url = settings.STATIC_URL	
		good_list = create_bonus_dict(request)
		choose_pay_url = CHOOSE_PAY_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		openid = open_id
		menu = _MenuUrl()
		return render_to_response('random_bonus.html', locals())	
	except:
		log_print(display_random_bonus_views) 
		return HttpResponseBadRequest('Bad request')		

@csrf_exempt
def view_redirect_random_bonus(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_random_bonus_views(openid, request)	
	
#发手气红包
@csrf_exempt
def view_random_bonus(request):
	#print("========view_random_bonus =========\n")
	return check_session_openid(request, REDIRECT_RB_URL, display_random_bonus_views)
	
def display_bonus_detail(open_id, request):
	try:
		title = '串串明细'
		openid = open_id	
		id_bonus = request.session['id_bonus']
		static_url = settings.STATIC_URL	
		snd_bonus = SndBonus.objects.get(id_bonus=id_bonus)
		rcv_bonus_list = RcvBonus.objects.filter(snd_bonus=snd_bonus, is_receive=True)
		ajax_request_url = AJAX_REQUEST_POST_URL
		menu = _MenuUrl()
		return render_to_response('bonus_detail_info.html', locals())
	except:
		log_print(display_bonus_detail) 
		return HttpResponseBadRequest('Bad request')		
	
@csrf_exempt
def view_redirect_bonus_detail(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_bonus_detail(openid, request)	
	
#串串详情
@csrf_exempt
def view_bonus_detail(request):
	#print("========view_bonus_detail =========\n")
	if 'id_bonus' in request.GET:
		request.session['id_bonus'] = request.GET.get('id_bonus')
	return check_session_openid(request, REDIRECT_BD_URL, display_bonus_detail)
	
def display_self_rcv_bonus(open_id, request):
	try:
		title = '收到的串串'
		openid = open_id
		static_url = settings.STATIC_URL
		consumer = Consumer.objects.get(open_id=openid)
		rcv_bonus_list = RcvBonus.objects.filter(consumer=consumer).order_by("datetime").reverse()
		bonus_detail_url = BONUS_DETAIL_URL
		menu = _MenuUrl()	
		return render_to_response('self_rcv_bonus.html', locals())	
	except:
		log_print(display_self_rcv_bonus) 
		return HttpResponseBadRequest('Bad request')	

@csrf_exempt	
def view_redirect_self_rcv_bonus(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_self_rcv_bonus(openid, request)		
	
#check收到的串串
@csrf_exempt
def view_self_rcv_bonus(request):
	#print("========view_self_rcv_bonus =========\n")	
	return check_session_openid(request, REDIRECT_SRB_URL, display_self_rcv_bonus)
	
def display_self_snd_bonus(open_id, request):
	try:
		title = '发出的串串'
		openid = open_id
		static_url = settings.STATIC_URL
		consumer = Consumer.objects.get(open_id=openid)
		snd_bonus_list = SndBonus.objects.filter(consumer=consumer).order_by("create_time").reverse()
		bonus_detail_url = BONUS_DETAIL_URL
		menu = _MenuUrl()	
		return render_to_response('self_snd_bonus.html', locals())	
	except:
		log_print(display_self_snd_bonus) 
		return HttpResponseBadRequest('Bad request')		

@csrf_exempt	
def view_redirect_self_snd_bonus(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_self_snd_bonus(openid, request)		

#check发出的串串
@csrf_exempt
def view_self_snd_bonus(request):
	#获取openid
	#print("========view_self_rcv_bonus =========\n")	
	return check_session_openid(request, REDIRECT_SSB_URL, display_self_snd_bonus)

def display_self_bonus_list(open_id, request):
	title = '串串排行榜'
	static_url = settings.STATIC_URL
	openid = open_id
	try:
		bonus_range = 1
		consumer_list = Consumer.objects.filter(is_admin=False).order_by("rcv_bonus_num").reverse()
		for consumer in consumer_list:
			consumer.bonus_range = bonus_range
			bonus_range += 1
			consumer.save()
		oneself = Consumer.objects.get(open_id=openid)
		top_consumer = consumer_list[0]
		menu = _MenuUrl()
		return render_to_response('self_bonus_list.html', locals())
	except:
		log_print(display_self_bonus_list) 
		return HttpResponseBadRequest('Bad request')
	
@csrf_exempt
def view_redirect_self_bonus_list(request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	request.session['openid'] = openid
	return display_self_bonus_list(openid, request)	
	
#check串串排行榜
@csrf_exempt
def view_self_bonus_list(request):
	#print("========view_self_bonus_list =========\n")	
	return check_session_openid(request, REDIRECT_SBL_URL, display_self_bonus_list)
		
#网页ajax请求
@csrf_exempt
def view_ajax_request(request):	
	#print('***view_ajax_request body: ****\n')
	log_print(view_ajax_request, log_level=1, message="%s"%(request.body))
	try:
		data = json.loads(request.body)
		action = data['action']
		#for key, value in data.items():
			#print('%s ==> %s'%(key, value))	
		#实现ajax请求处理函数
		response = handle_ajax_request(action, data, request)

		return HttpResponse(response)
	except:
		log_print(view_ajax_request) 
		return HttpResponseBadRequest('Bad request')
	
#抢到的红包界面
@csrf_exempt
def view_geted_bonus(request):
	if "id_record" in request.session:
		try:
			id_record = request.session['id_record']
			#print("===view_geted_bonus:%s===\n"%(id_record))
			title = '抢到的红包'
			static_url = settings.STATIC_URL
			bonus_dir = check_geted_bonus(id_record)
			openid = get_record_openid(id_record)
			random_bonus = bonus_dir['random_bonus']
			common_bonus = bonus_dir['common_bonus']
			system_bonus = bonus_dir['system_bonus']	
			common_bonus_url = CREATE_COMMON_BONUS_URL
			ajax_request_url = AJAX_REQUEST_POST_URL
			#del request.session['id_record']
			menu = _MenuUrl()
			return render_to_response('geted_bonus.html', locals())
		except:
			log_print(view_geted_bonus) 
			return HttpResponseBadRequest('Bad request')		
	else:
		return check_session_openid(request, REDIRECT_BR_URL, display_rcv_bonus_views)

#支付页面
@csrf_exempt	
def view_choose_pay(request):
	try:
		openid = request.session['openid']
		consumer = Consumer.objects.get(open_id=openid)
		title = '支付'
		body_class = 'qubaba_hsbj'
		static_url = settings.STATIC_URL
		data_dict = request.session['consumer_order']
		result_dir = decode_choose_pay(request, data_dict)
		good_list = result_dir['good_list']
		total_money = result_dir['total_money']
		enough_money = is_enough_pay(consumer, request.GET)
		snd_bonus_url = SND_BONUS_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		menu = _MenuUrl()
		return render_to_response('weixin_pay.html', locals())
	except:
		log_print(view_choose_pay) 
		return HttpResponseBadRequest('Bad request')	
	
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

