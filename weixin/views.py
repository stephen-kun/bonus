# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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
from .utils import check_geted_bonus, decode_order_param, get_bonus_type_str, get_record_openid, is_enough_pay, log_print
from .models import DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus
from wzhifuSDK import *
from .wx_config import *
from .utils import gen_trade_no , snd_bonus_pay_weixin
from lxml import etree
import types



class _MenuUrl():
	get_bonus_url = GET_BONUS_URL
	snd_bonus_url = SND_BONUS_URL
	settle_accounts_url = SETTLE_ACCOUNTS_URL
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

def _response_json(state, message):
	data = {}
	data['state'] = state
	data['message'] =  message
	return HttpResponse(json.dumps(data), content_type="application/json")

#验券接口
@csrf_exempt
def check_consumer_code(request):
	try:
		print request.body
		#data_dict = json.loads(request.body)
		id_ticket = request.POST.get('ticket_code') 
		print id_ticket
		ticket = Ticket.objects.filter(id_ticket=id_ticket)
		ticket_value = float(0)
		response = {}
		if len(ticket) and (ticket[0].is_consume):
			return _response_json(1, "该券已使用")
		elif len(ticket) and (ticket[0].is_consume == False):
			ticket_value = ticket[0].ticket_value
			ticket[0].is_consume = True
			ticket[0].save()
			return _response_json(0, "券可抵扣%d"%ticket_value)
		else:
			return _response_json(2, "券码错误")

	except Exception as e:
		# 生成日志
		log_print(check_consumer_code)
		return _response_json(3, "错误")

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
	
def display_redirect_views(view_func,request):
	openid = get_user_openid(request, ACCESS_TOKEN_URL)
	if openid:
		request.session['openid'] = openid
	else:
		openid = request.session['openid']
	return view_func(openid, request)	
	
#我的个人界面
@csrf_exempt
def view_user_account(request):	
	return view_redirect_func(REDIRECT_UA_URL)
	
@csrf_exempt
def view_redirect_user_account(request):	
	return display_redirect_views(display_user_account_views, request)
	
def display_user_account_views(open_id, request):
	try:
		title = '我'
		openid = open_id
		static_url = settings.STATIC_URL	
		consumer = Consumer.objects.get(open_id=openid)
		good_list = decode_bonus_detail(consumer)
		user_ticket_url = USER_TICKET_URL
		user_info_url = USER_INFO_URL
		menu = _MenuUrl()
		return render_to_response('user_account.html', locals())	
	except:
		log_print(display_user_account_views) 
		return HttpResponseBadRequest('Bad request')	
	
#发红包界面	
@csrf_exempt
def view_snd_bonus(request):
	#print('---**view_snd_bonus**---\n')
	return view_redirect_func(REDIRECT_BS_URL)	

@csrf_exempt
def view_redirect_bonus_snd(request): 
	return display_redirect_views(display_snd_bonus_views, request)	
	
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
		
#抢红包界面
@csrf_exempt
def view_rcv_bonus(request):
	#print('---**view_rcv_bonus**---\n')
	return view_redirect_func(REDIRECT_BR_URL)	
	
@csrf_exempt
def view_redirect_bonus_rcv(request):
	return display_redirect_views(display_rcv_bonus_views, request)	
	
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
	
#结算界面
@csrf_exempt
def view_settle_account(request):	
	#print('---**view_settle_account**---\n')
	return view_redirect_func(REDIRECT_SA_URL)
	
@csrf_exempt
def view_redirect_settle_account(request):	
	return display_redirect_views(display_settle_account_views,  request)		

def display_settle_account_views(open_id, request):	
	openid = open_id
	try:
		if is_consumer_dining(openid):		
			title = '结算'
			static_url = settings.STATIC_URL
			consumer = Consumer.objects.get(open_id=openid)
			ajax_request_url = AJAX_REQUEST_POST_URL
			menu = _MenuUrl()
			return render_to_response('close_an_account.html', locals())		
		else:
			prompt_message = '就餐用户独享抢红包！'
			return display_prompt_views(prompt_message)	
	except:
		log_print(display_settle_account_views) 
		return HttpResponseBadRequest('Bad request')
	
#论坛界面
@csrf_exempt
def view_qubaba_forum(request):
	return view_redirect_func(REDIRECT_QF_URL)
	
@csrf_exempt
def view_redirect_qubaba_forum(request):	
	return display_redirect_views(display_qubaba_forum_views,  request)		
	
def display_qubaba_forum_views(open_id, request):
	url = 'http://wx.tonki.com.cn/wx/?open_id=%s'%(open_id)
	return HttpResponseRedirect(url)
	
def display_prompt_views(message):
	title = '提示'
	static_url = settings.STATIC_URL
	prompt_message = message
	menu = _MenuUrl()
	return render_to_response("user_prompt.html", locals())		

#******************************************************************************	

def check_session_openid(request, redirect_uri, redirect_func):
	if 'openid' in request.session:
		openid = request.session['openid']
		return redirect_func(openid, request)
	else:
		url = OAUTH_URL.replace('REDIRECT_URL', redirect_uri)
		return HttpResponseRedirect(url)
	
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
	return display_redirect_views(display_user_info,  request)	
	
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
		ticket_list = consumer.own_ticket_list
		ticket_num = len(ticket_list)
		menu = _MenuUrl()
		return render_to_response('user_ticket.html', locals())	
	except:
		log_print(display_user_ticket) 
		return HttpResponseBadRequest('Bad request')	
	
@csrf_exempt
def view_redirect_user_ticket(request):
	return display_redirect_views(display_user_ticket,  request)		

#我的消费券
@csrf_exempt
def view_user_ticket(request):
	#print('---**view_user_ticket**---\n')
	return check_session_openid(request, REDIRECT_UT_URL, display_user_ticket)	
	
	
def display_common_bonus_views(open_id, request):
	try:
		title = '普通红包'
		static_url = settings.STATIC_URL
		good_list = create_bonus_dict(request)
		ajax_request_url = AJAX_REQUEST_POST_URL
		choose_pay_url = WEIXIN_PAY_URL
		pay_suc_url = SND_BONUS_URL
		openid = open_id
		menu = _MenuUrl()
		return render_to_response('common_bonus.html', locals())	
	except:
		log_print(display_common_bonus_views) 
		return HttpResponseBadRequest('Bad request')		
	
@csrf_exempt
def view_redirect_common_bonus(request):
	return display_redirect_views(display_common_bonus_views,  request)	
		
#发普通红包
@csrf_exempt
def view_common_bonus(request):
	return check_session_openid(request, REDIRECT_CB_URL, display_common_bonus_views)
	
def display_random_bonus_views(open_id, request):
	try:
		title = '手气红包'
		static_url = settings.STATIC_URL	
		good_list = create_bonus_dict(request)
		choose_pay_url = WEIXIN_PAY_URL
		ajax_request_url = AJAX_REQUEST_POST_URL
		pay_suc_url = SND_BONUS_URL
		openid = open_id
		menu = _MenuUrl()
		return render_to_response('random_bonus.html', locals())	
	except:
		log_print(display_random_bonus_views) 
		return HttpResponseBadRequest('Bad request')		

@csrf_exempt
def view_redirect_random_bonus(request):
	return display_redirect_views(display_random_bonus_views,  request)	
	
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
	return display_redirect_views(display_bonus_detail,  request)	
	
#串串详情
@csrf_exempt
def view_bonus_detail(request):
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
	return display_redirect_views(display_self_rcv_bonus,  request)	
	
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
	return display_redirect_views(display_self_snd_bonus,  request)	

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
	return display_redirect_views(display_self_bonus_list,  request)	
	
#check串串排行榜
@csrf_exempt
def view_self_bonus_list(request):
	#print("========view_self_bonus_list =========\n")	
	return check_session_openid(request, REDIRECT_SBL_URL, display_self_bonus_list)
	
#页内发红包
def site_snd_bonus(request):
	return check_session_openid(request, REDIRECT_BS_URL, display_snd_bonus_views)
	
#页内收发红包
def site_rcv_bonus(request):
	return check_session_openid(request, REDIRECT_BR_URL, display_rcv_bonus_views)

#页内结算
def site_settle_account(request):
	return check_session_openid(request, REDIRECT_SA_URL, display_settle_account_views)

#页内查看我
def site_user_account(request):
	return check_session_openid(request, REDIRECT_UA_URL, display_user_account_views)	
		
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
def view_test_wxpay(request):
	openid = request.session['openid']
	#openid = "oxxmTw-fh_5DHSJzm-dq619BumSE"
	static_url = settings.STATIC_URL
	wx_order=UnifiedOrder_pub()
	param_dict={}
	trade_no = gen_trade_no()
	wx_order.setParameter("out_trade_no", trade_no)
	wx_order.setParameter("body", "pay test")
	wx_order.setParameter('total_fee', '1')
	wx_order.setParameter('notify_url', 'http://wx.tonki.com.cn/weixin/pay_notify/')
	wx_order.setParameter('trade_type','JSAPI')
	wx_order.setParameter('openid', openid)
	wx_order.setParameter('spbill_create_ip', request.META['REMOTE_ADDR'])
	prepay_id=wx_order.getPrepayId()

	jsapi_pub=JsApi_pub()
	jsapi_pub.setPrepayId(prepay_id)	
	param_json = jsapi_pub.getParameters()
	return render_to_response('test_weixin_pay.html', locals())

#支付页面
@csrf_exempt	
def view_weixin_pay(request):
	try:
		openid = request.session['openid']
		consumer = Consumer.objects.get(open_id=openid)
		title = '支付'
		static_url = settings.STATIC_URL
		data_dict = request.session['consumer_order']
		result_dir = decode_order_param(data_dict)
		good_list = result_dir['good_list']
		total_money = result_dir['total_money']
		ajax_request_url = AJAX_REQUEST_POST_URL
		prepay_id = request.session['prepay_id']
		pay_suc_url = SND_BONUS_URL
		menu = _MenuUrl()
		if TEST_DEBUG:
			return render_to_response('test_weixin_pay.html', locals())
		else:
			jsapi_pub=JsApi_pub()
			jsapi_pub.setPrepayId(prepay_id)	
			pay_param = jsapi_pub.getParameters()				
			return render_to_response('weixin_pay.html', locals())			
	except:
		log_print(view_weixin_pay) 
		return HttpResponseBadRequest('Bad request')	
	
@csrf_exempt
def view_wechat_token(request):
	try:
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
	except:
		log_print(view_wechat_token)
		return HttpResponseBadRequest('Verify Failed')

@csrf_exempt
def view_pay_notify(request):
	log_print(view_pay_notify, log_level=1, message="%s"%(request.body))
	notify=Notify_pub()
	try:
		notify.saveData(request.body)
		if(notify.checkSign()):
			#判断通知订单已经处理
			return_code = notify.data['return_code']
			out_trade_no = notify.data['out_trade_no']
			recharge = Recharge.objects.filter(out_trade_no=out_trade_no, status=False)
			if len(recharge) and return_code == 'SUCCESS':
				new_recharge = Recharge.objects.get(out_trade_no=out_trade_no)
				consumer_order = json.loads(new_recharge.consumer_order)	
				recharge.update(status=True, trade_state=notify.data['result_code'], total_fee=notify.data['total_fee'])
				consumer = new_recharge.recharge_person
				if notify.data['result_code'] == 'SUCCESS':
					#充值进客户账号
					new_recharge.charge_money
					if consumer.session:
						#支付成功业务
						snd_bonus_pay_weixin(consumer_order)
				else:
					#支付失败业务
					pass						
			notify.setReturnParameter("return_code", "SUCCESS")
			notify.setReturnParameter("return_msg", "OK")
		else:
			notify.setReturnParameter("return_code", "FAIL")
			notify.setReturnParameter("return_msg", u"SIGNERROR")
	except: 
		log_print(view_pay_notify)
		notify.setReturnParameter("return_code", "FAIL")
		notify.setReturnParameter("return_msg", "ARGSERROR")
	return HttpResponse(notify.returnXml(), content_type="application/xml") 





