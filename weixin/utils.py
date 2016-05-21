# -*- coding: utf-8 -*-
# utils.py
# Create your utils here.

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import random, string
from django.core.exceptions import ObjectDoesNotExist 
from .models import DiningTable,Consumer,VirtualMoney, WalletMoney, AuthCode
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus

import datetime
import time
import re
import urllib2
import json
import pytz
import traceback
from django.utils import timezone

from wzhifuSDK import *

COMMON_BONUS = 0
RANDOM_BONUS = 1
SYS_BONUS	= 2

WEIXIN_PAY = '0'
WALLET_PAY = '1'

SUCCESS = 'SUCCESS'
FAIL = 'FAIL'
NOTPAY = 'NOTPAY'
CLOSED = 'CLOSED'
REFUND = 'REFUND'
USERPAYING = 'USERPAYING'
PAYERROR = 'PAYERROR'


AJAX_GET_BONUS = 'ajax_get_bonus'
AJAX_CREATE_TICKET = 'ajax_create_ticket'
AJAX_WEIXIN_PAY = 'ajax_weixin_pay'
AJAX_BONUS_REFUSE = 'ajax_bonus_refuse'
AJAX_BONUS_MESSAGE = 'ajax_bonus_message'
AJAX_MODIFY_PHONE = 'ajax_modify_phone'
AJAX_MODIFY_NAME = 'ajax_modify_name'
AJAX_MODIFY_ADDRESS = 'ajax_modify_address'
AJAX_MODIFY_EMAIL = 'ajax_modify_email'
AJAX_MODIFY_SEX = 'ajax_modify_sex'
AJAX_WEIXIN_ORDER = 'ajax_weixin_order'


class _GetedBonus():
	def __init__(self, rcv_bonus):
		self.id_bonus = rcv_bonus.id_bonus
		self.openid = rcv_bonus.consumer.open_id
		self.name = rcv_bonus.snd_bonus.consumer.name
		self.picture = rcv_bonus.snd_bonus.consumer.picture
		self.message = rcv_bonus.snd_bonus.to_message
		self.datetime = rcv_bonus.datetime
		self.title = rcv_bonus.snd_bonus.title
		l_content = bonus_content_json_to_models(rcv_bonus.content)
		self.content = l_content

class _Bonus():
	def __init__(self, open_id=None, bonus_type=0, content=None, table=None, message=None, money=0, bonus_num=0, number=0):
		self.open_id = open_id
		self.bonus_type = bonus_type
		self.content = content
		self.table = table
		self.message = message
		self.money = money
		self.bonus_num = bonus_num
		self.number = number		#串串个数

class _BonusContent():
	def __init__(self, name=None, price=None, unit=None, number=0):
		self.name = name
		self.price = price
		self.unit = unit
		self.number = number

#日志存储
def log_print(back_func, log_level=3, message=None):
	path = './log/FILE.txt'.replace('FILE', back_func.__name__)
	f = open(path, 'a')
	f.write(time.strftime('===============%Y-%m-%d %H:%M============\n', time.localtime(time.time())))
	if log_level >= 3:
		traceback.print_exc(file=f)
	else:
		f.write(message)
		f.write('\n')
	f.flush()
	f.close()

#VirtualMoney 转换为红包内容
def virtual_money_to_bonus_content():
	virtual_money = VirtualMoney.objects.all()
	l_content = []

	for money in virtual_money:
		content = _BonusContent()
		content.name = money.name
		content.price = money.price
		content.unit = money.unit
		content.number = 0
		l_content.append(content)

	return l_content


#红包内容 models转换为json
def bonus_content_models_to_json(models_list):
	l_name = []
	l_bonus = []
	l_content = virtual_money_to_bonus_content()

	for content in l_content:
		for money in models_list:
			if money.money.name == content.name:
				content.number += 1
		bonus = dict(name=content.name, price=content.price, unit=content.unit, number=content.number)
		l_name.append(content.name)
		l_bonus.append(bonus)

	return json.dumps(dict(zip(l_name, l_bonus)))

#红包内容json转换为models
def bonus_content_json_to_models(json_content):
	dict_content = json.loads(json_content)
	l_content = []
	for value in dict_content.itervalues():
		content = _BonusContent()
		content.name = value['name']
		content.price = value['price']
		content.unit = value['unit']
		content.number = value['number']
		l_content.append(content)
	return l_content



#判断用户是否有足够零钱支付红包
def is_enough_pay(consumer, total_money):
	if consumer.own_bonus_value >= total_money:
		return True
	else:
		return False


def get_record_openid(id_record):
	record_rcv_bonus = RecordRcvBonus.objects.get(id_record=id_record)
	return record_rcv_bonus.consumer.open_id

#ajax请求参数检测
def check_ajax_params(src_keys, dest_dict):
	for key in src_keys:
		if dest_dict.has_key(key):
			pass
		else:
			return False
	return True


#获取用户openid
def get_user_openid(request, access_token_url):
	try:
		code = request.GET.get(u'code')
		url = access_token_url.replace('CODE', code)
		response = urllib2.urlopen(url)
		content = response.read()
		access_token = json.loads(content)
		openid = access_token['openid']
		return openid
	except:
		log_print(get_user_openid)
		return None


#检测用户是否在就餐状态
def is_consumer_dining(openid):
	try:
		consumer = Consumer.objects.get(open_id=openid)
		if consumer.on_table:
			return consumer.on_table.status
		else:
			return False
	except ObjectDoesNotExist:
		return False


#主键生成方法
def create_primary_key(length=10):
	a = list(string.digits)
	random.shuffle(a)
	primary = ''.join(a[:length])
	return primary

#统计餐桌抢到的所有红包金额
def count_total_money_on_table(openid):
	consumer = Consumer.objects.get("openid")
	table = consumer.on_table
	consumer_list = Consumer.objects.filter(on_table=table)



#查看抢到的红包
def check_geted_bonus(id_record):
	#print('*******check_geted_bonus********')
	record_rcv_bonus = RecordRcvBonus.objects.get(id_record=id_record)
	rcv_bonus_list = RcvBonus.objects.filter(record_rcv_bonus=record_rcv_bonus)
	random_bonus = []
	common_bonus = []
	system_bonus = []
	for bonus in rcv_bonus_list:
		geted_bonus = _GetedBonus(bonus)
		if bonus.bonus_type == COMMON_BONUS:
			common_bonus.append(geted_bonus)
		elif bonus.bonus_type == RANDOM_BONUS:
			random_bonus.append(geted_bonus)
		elif bonus.bonus_type == SYS_BONUS:
			system_bonus.append(geted_bonus)
		else:
			#print('===can not match==\n')
			pass
	return dict(random_bonus=random_bonus, common_bonus=common_bonus, system_bonus=system_bonus)

#获取红包类型字符串
def get_bonus_type_str(bonus_type):
	if bonus_type == 0:
		return "普通红包"
	elif bonus_type == 1:
		return "手气红包"
	else:
		return "系统红包"


#红包留言
def action_bonus_message(data):
	id_bonus = data["id_bonus"]
	message = data["message"]
	log_print(back_func=action_bonus_message, log_level=1, message='id-%s msg-%s'%(id_bonus, message))
	rcv_bonus = RcvBonus.objects.get(id_bonus=id_bonus)
	rcv_bonus.message = message
	rcv_bonus.is_message = True
	rcv_bonus.save()
	return "ok"
	

#红包婉拒
def action_bonus_refuse(data):
	id_bonus = data['id_bonus']
	rcv_bonus = RcvBonus.objects.get(id_bonus=id_bonus)
	rcv_bonus.bonus_refuse()
	return 'refuse ok'
		

#随机分配红包算法
def get_random_bonus(money_num, bonus_num):
	l_money = []
	while bonus_num:
		if bonus_num == 1:
			l_money.append(money_num)
			return l_money

		money_min = 1
		money_max = int(money_num/bonus_num*2)
		rand = random.random()
		money = int(money_max*rand)
		if money < money_min:
			money = money_min
		l_money.append(money)
		bonus_num -= 1
		money_num -= money
	return l_money

#将红包分拆
def snd_bonus_random_rcv_bonus(snd_bonus, number_list):
	number_list.sort(reverse=True)
	is_best = True
	total_number = 0
	total_value = 0
	for number in number_list: 

		total_money = 0
		rcv_bonus = RcvBonus.objects.create(id_bonus=create_primary_key(), snd_bonus=snd_bonus)
		money_list = WalletMoney.objects.filter(snd_bonus=snd_bonus, is_receive=False)[0:number]
		account = 0	#统计串串个数
		for money in money_list:
			money.rcv_bonus = rcv_bonus
			money.is_receive = True 
			#if money.money.name == LIST_KEY_ID:
			account += 1
			money.save()
			total_money += money.money.price
		rcv_bonus.bonus_type = snd_bonus.bonus_type
		rcv_bonus.number = account
		rcv_bonus.total_money = total_money
		if is_best and (rcv_bonus.bonus_type != COMMON_BONUS):
			rcv_bonus.is_best = True
			is_best = False
		rcv_bonus.content = bonus_content_detail(bonus=rcv_bonus, type='rcv')
		rcv_bonus.save()
		total_number += account
		total_value += total_money
	snd_bonus.consumer.snd_bonus_num += total_number
	snd_bonus.consumer.snd_bonus_value += total_value
	snd_bonus.consumer.save()
	
#更新用户钱包余额
def update_wallet_money(consumer):
	money_list = WalletMoney.objects.filter(consumer=consumer, is_used=False, is_valid=True, is_send=False)
	sum_money = float(0)
	for money in money_list:
		price = money.money.price
		sum_money += price

	consumer.own_bonus_value = sum_money
	consumer.save()
	return consumer

#结算操作
def close_an_account(consumer, ticket, ticket_value):
	sum = float(0) 			#统计金额
	is_remain = False			#是否结余
	#查找就餐会话中抢到的所有红包
	rcv_bonus_list = RcvBonus.objects.filter(session=consumer.session)
	for bonus in rcv_bonus_list:
		money_list = WalletMoney.objects.filter(rcv_bonus=bonus, is_used=False, is_valid=True)
		for money in money_list:
			if is_remain:
				money.consumer = consumer
				money.ticket = None
				money.is_send = False
				money.is_receive = False
				money.snd_bonus = None
				money.rcv_bonus = None
				money.save()
			else:
				price = money.money.price
				sum += price
				if sum > ticket_value:
					sum -= price
					is_remain = True
					money.consumer = consumer
					money.ticket = None
					money.is_send = False
					money.is_receive = False
					money.snd_bonus = None
					money.rcv_bonus = None
					money.save()
				else:
					money.ticket = ticket
					money.consumer = consumer
					money.save()

	#使用钱包余额
	if is_remain == False:
		wallet_list = WalletMoney.objects.filter(consumer=consumer, is_used=False, is_valid=True, ticket=None)
		for money in wallet_list:
			price = money.money.price
			sum += price
			if sum > ticket_value:
				sum -= price
				break
			else:
				money.ticket = ticket
				money.save()
	return sum

#红包退回操作
def bonus_snd_back(rcv_bonus_list):
	for rcv_bonus in rcv_bonus_list:
		money_list = WalletMoney.objects.filter(rcv_bonus=rcv_bonus)
		for money in money_list:
			money.snd_bonus = None
			money.rcv_bonus = None
			money.is_send = False
			money.is_receive = False
			money.save()


#创建消费券事件
def action_create_ticket(data):
	src_keys = ['openid', 'user_wallet', 'total_money','ticket_value', 'auth_code']
	if check_ajax_params(src_keys, data):
		openid = data['openid']
		consumer = Consumer.objects.get(open_id=openid)
		ticket_value = float(data['ticket_value'])
		auth_code = data['auth_code']
		code = AuthCode.objects.filter(id_code=auth_code)
		if len(code) == 0:
			return dict(status=2, error_message="验证码错误，请重新输入！")

		#生成一条消费券记录
		new_ticket = Ticket.objects.create(id_ticket=create_primary_key(), valid_time=timezone.now())
		new_ticket.consumer = consumer

		#结算操作
		ticket_value = close_an_account(consumer, new_ticket, ticket_value)
		new_ticket.ticket_value = ticket_value
		new_ticket.save()

		#失效该就餐会话发出的红包，将未抢红包以及婉拒红包返回客户账号
		snd_bonus_list = SndBonus.objects.filter(session=consumer.session, is_exhausted=False)
		for snd_bonus in snd_bonus_list:
			snd_bonus.is_valid = False
			snd_bonus.save()
			rcv_bonus_list = RcvBonus.objects.filter(snd_bonus=snd_bonus, is_receive=False)
			bonus_snd_back(rcv_bonus_list)

		#婉拒红包退回
		refuse_bonus_list = RcvBonus.objects.filter(is_refuse=True)
		bonus_snd_back(refuse_bonus_list)

		#关闭就餐会话，释放桌台
		consumer.session.over_time = timezone.now()
		consumer.session.save()
		consumer.on_table.status = False
		consumer.on_table.save()
		consumer_list = Consumer.objects.filter(session=consumer.session)
		for user in consumer_list:
			#print("++++++++++++清会话以及桌台+++++++++++++++++")
			user.on_table = None
			user.session = None
			user.save()
		
		#更新用户钱包余额及明细
		new_consumer = Consumer.objects.get(open_id=openid)	
		new_consumer.update_info

		#返回消费券码以及券值
		id_ticket = str(new_ticket.id_ticket)
		return dict(status=0, ticket_value=ticket_value, part1=id_ticket[0:3], part2=id_ticket[3:6], part3=id_ticket[6:10])
	else:
		return dict(status=1, error_message="参数错误")

def update_bonus_dict_to_session(request, update_dir):
	l_name = []
	l_content = []
	for key, value in update_dir.items():
		l_name.append(key)
		content = dict(name=value.name, price=value.price, unit=value.unit, number=value.number)
		content = json.dumps(content)
		l_content.append(content)
	request.session['create_bonus'] = dict(zip(l_name, l_content))

def create_bonus_session_to_dict(request):
	create_bonus = request.session['create_bonus']
	l_name = []
	l_money = []
	for key,value in create_bonus.items():
		l_name.append(key)
		content = _BonusContent()
		temp = json.loads(value)
		content.name = temp['name']
		content.price = temp['price']
		content.unit = temp['unit']
		l_money.append(content)
	return dict(zip(l_name, l_money))

def create_bonus_dict_to_session(request):
	virtual_money = VirtualMoney.objects.all()
	l_name = []
	l_money = []
	l_content = []
	for money in virtual_money:
		l_name.append(money.name)
		l_money.append(money)
		content = dict(name=money.name, price=money.price, unit=money.unit, number=0)
		content = json.dumps(content)
		l_content.append(content)
	request.session['create_bonus'] = dict(zip(l_name, l_content))
	return dict(zip(l_name, l_money))

#创建红包内容的字典
def create_bonus_dict(request):
	return create_bonus_dict_to_session(request)
	'''
	if "create_bonus" in request.session:
		#print("***session create_bonus****")
		return create_bonus_session_to_dict(request)
	else:
		return create_bonus_dict_to_session(request)
	'''

#我的钱包内容字符串
def decode_bonus_detail(consumer):
	bonus_detail = consumer.own_bonus_detail
	l_content = []
	if bonus_detail:
		l_content = bonus_content_json_to_models(bonus_detail)
	return l_content

#生成红包内容字符串
def bonus_content_detail(bonus=None, consumer=None, type='rcv'):
	'''
	type : snd 表示发送的红包，rcv 表示接收的红包, own 表示拥有的红包
	'''
	wallet_money = None
	if type == 'snd':
		wallet_money = WalletMoney.objects.filter(snd_bonus=bonus)
	elif type == 'rcv':
		wallet_money = WalletMoney.objects.filter(rcv_bonus=bonus)
	elif type == 'own':
		wallet_money = WalletMoney.objects.filter(consumer=consumer, is_used=False, is_valid=True, is_send=False)

	return bonus_content_models_to_json(wallet_money)


#展现抢到的红包
def display_get_bonus(id_record, bonus_type):
	'''
	bonus_type: 0:普通红包， 1:手气红包， 2:系统红包
	'''
	bonus_list = []
	try:
		record_rcv_bonus = RecordRcvBonus.objects.get(id_record=id_record)
		rcv_bonus = RcvBonus.objects.filter(bonus_type=bonus_type, record_rcv_bonus=record_rcv_bonus)
		for bonus in rcv_bonus:
			geted_bonus = _GetedBonus(rcv_bonus=bonus)
			bonus_list.append(geted_bonus)
	except ObjectDoesNotExist:
		pass
	return bonus_list

#抢红包
def get_bonus(consumer, session, record_rcv_bonus, bonus_list, param_tuple):
	bonus_num = param_tuple[0]
	total_money = param_tuple[1]
	total_number = param_tuple[2]
	if len(bonus_list):
		for bonus in bonus_list:
			#判断该红包是否能抢
			get_bonus = RcvBonus.objects.filter(snd_bonus=bonus, consumer=consumer)
			if len(get_bonus):
				continue
			remain_bonus = RcvBonus.objects.filter(snd_bonus=bonus).exclude(is_receive=True)
			length = len(remain_bonus)
			if length:
				rand = random.randint(0, (length-1))
				bonus_num += 1
				total_money += remain_bonus[rand].total_money
				total_number += remain_bonus[rand].number
				remain_bonus[rand].consumer = consumer
				remain_bonus[rand].datetime = timezone.now()
				remain_bonus[rand].session = session
				remain_bonus[rand].record_rcv_bonus = record_rcv_bonus
				remain_bonus[rand].is_receive = True
				remain_bonus[rand].save()
				if bonus.bonus_remain == 1:
					bonus.is_exhausted = True
					bonus.over_time = timezone.now()
					bonus.is_valid = False
				bonus.bonus_remain -= 1
				bonus.bonus_exhausted += 1
				bonus.save()
	return [bonus_num, total_money, total_number]

#抢红包事件
def action_get_bonus(openid, request):

	#返回抢到的红包个数
	bonus_num = 0			#统计抢到的红包个数
	total_number = 0		#统计串串个数
	total_money = 0 		#统计抢到的红包总额

	consumer = Consumer.objects.get(open_id=openid)

	#准备一条抢红包记录
	record_rcv_bonus = RecordRcvBonus.objects.create(id_record=create_primary_key(), consumer=consumer)

	#过滤能够抢的各类红包
	common_bonus_list = SndBonus.objects.filter(is_exhausted=False, is_valid=True, bonus_type=COMMON_BONUS).exclude(consumer=consumer)
	random_bonus_list = SndBonus.objects.filter(is_exhausted=False, is_valid=True, bonus_type=RANDOM_BONUS)
	system_bonus_list = SndBonus.objects.filter(is_exhausted=False, is_valid=True, bonus_type=SYS_BONUS)

	#分配红包
	param_list = [bonus_num, total_money, total_number]
	param_list = get_bonus(consumer, consumer.session, record_rcv_bonus,common_bonus_list, param_list)
	param_list = get_bonus(consumer, consumer.session, record_rcv_bonus,random_bonus_list, param_list)
	param_list = get_bonus(consumer, consumer.session, record_rcv_bonus,system_bonus_list, param_list)
	bonus_num = param_list[0]
	total_money = param_list[1]
	total_number = param_list[2]

	if bonus_num:
		#更新session信息
		consumer.session.total_bonus += bonus_num
		consumer.session.total_money += total_money
		consumer.session.total_number += total_number
		consumer.session.save()
		consumer.rcv_bonus_num += total_number
		consumer.rcv_bonus_value += total_money
		consumer.save()

		#更新抢红包记录
		record_rcv_bonus.bonus_num = bonus_num
		record_rcv_bonus.save()

		#存储django session
		request.session['id_record'] = record_rcv_bonus.id_record

	response = dict(status=0, number=bonus_num)
	return json.dumps(response)

#生成虚拟货币
def create_vitural_money(consumer, snd_bonus, recharge, money, number, is_send):
	#print("***create_vitural_money %s**"%(number))
	for x in range(int(number)):
		wallet_money = WalletMoney(id_money=create_primary_key(), consumer=consumer, recharge=recharge, snd_bonus=snd_bonus, money=money)
		wallet_money.is_send = is_send
		wallet_money.is_valid = True
		wallet_money.is_used = False
		wallet_money.save()

#将发红包内容存入session
def snd_bonus_to_session(request, bonus):
	snd_bonus = dict(bonus_type=bonus.bonus_type, table=bonus.table, message=bonus.message, money=bonus.money, bonus_num=bonus.bonus_num, content=bonus.content, number=bonus.number)
	snd_bonus = json.dumps(snd_bonus)
	request.session['snd_bonus'] = snd_bonus

#从session中解析出发红包内容
def snd_bonus_from_session(session):
	bonus = _Bonus()
	if 'snd_bonus' in session:
		snd_bonus = session['snd_bonus']
		snd_bonus = json.loads(snd_bonus)
		for key, value in snd_bonus.items():
			if key == 'table':
				bonus.table = value
			elif key == 'message':
				bonus.message = value
			elif key == 'money':
				bonus.money = value
			elif key == 'bonus_num':
				bonus.bonus_num = value
			elif key == "number":
				bonus.number = value
			elif key == 'content':
				bonus.content = value
			elif key == 'bonus_type':
				bonus.bonus_type = value
		return bonus
	else:
		return None

#解析支付请求
def decode_choose_pay(request, data_dir):
	#print("**** decode_choose_pay  *****")
	result = {}
	total_money = 0
	number = 0				#统计串串个数
	create_bonus = create_bonus_dict(request)
	bonus = _Bonus()
	for key, value in data_dir.items():
		if key in create_bonus:
			create_bonus[key].number = value
			price = float(create_bonus[key].price)
			num = int(value)
			total_money += price*num
			#if key == LIST_KEY_ID:
			number += int(value)
		else:
			if key == 'table':
				bonus.table = value
			elif key == 'message':
				bonus.message = value
			elif key == "bonus_num":
				bonus.bonus_num = value
			elif key == "bonus_type":
				bonus.bonus_type = value
	bonus.money = total_money
	bonus.number = number
	update_bonus_dict_to_session(request, create_bonus)
	content = request.session['create_bonus']
	bonus.content = content
	snd_bonus_to_session(request, bonus)
	result = dict(good_list=create_bonus, total_money=total_money)
	return result

def action_modify_phone(data):
	openid = data['openid']
	phone_num = data['phone_num']
	Consumer.objects.filter(open_id=openid).update(phone_num=phone_num)
	return ''

def action_modify_address(data):
	openid = data['openid']
	address = data['address']
	Consumer.objects.filter(open_id=openid).update(address=address)
	return ''

def action_modify_email(data):
	openid = data['openid']
	email = data['email']
	Consumer.objects.filter(open_id=openid).update(email=email)
	return ''

def action_modify_name(data):
	openid = data['openid']
	name = data['name']
	Consumer.objects.filter(open_id=openid).update(name=name)
	return ''

def action_modify_sex(data):
	openid = data['openid']
	sex = data['sex']
	Consumer.objects.filter(open_id=openid).update(sex=sex)
	return ''

#获得红包内容
def decode_order_param(data_dir):
	content_list = virtual_money_to_bonus_content()
	result = {}
	total_money = 0
	number = 0				#统计串串个数
	bonus = _Bonus()
	l_name = []
	l_content = []
	for key, value in data_dir.items():
		for content in content_list:
			if key == content.name:
				content.number = value
				total_money += float(content.price)*int(value)
				number += int(value)
			else:
				if key == 'table':
					bonus.table = value
				elif key == 'message':
					bonus.message = value
				elif key == "bonus_num":
					bonus.bonus_num = value
				elif key == "bonus_type":
					bonus.bonus_type = value	
			l_name.append(content.name)
			#s_content = json.dumps(dict(name=content.name, price=content.price, unit=content.unit, number=content.number))
			s_content = dict(name=content.name, price=content.price, unit=content.unit, number=content.number)
			l_content.append(s_content)					
	bonus.money = total_money
	bonus.number = number
	bonus.content = json.dumps(dict(zip(l_name, l_content)))
	result = dict(good_list=content_list, total_money=total_money, bonus_info=bonus)
	return result
	
def action_weixin_order(data, request):
	request.session['consumer_order'] = data
	order_info = decode_order_param(data)
	openid = data['openid']
	consumer = Consumer.objects.get(open_id=openid)
	total_money = order_info['total_money']
	bonus_info = order_info['bonus_info']
	response = {}
	if is_enough_pay(consumer, int(total_money)):
		#发红包
		consumer.snd_person_bonus(bonus_info=bonus_info)
		response = dict(status=0, pay_type=1, money=total_money)
	else:
		l_content = bonus_content_json_to_models(bonus_info.content)
		order_detail = "趣八八串串(%s元/%s):数量%s,总额%s"%(l_content[0].price, l_content[0].unit, l_content[0].number, total_money)
		#order_detail = 'QUBABA'
		# 调用微信统一下单接口
		total_fee = str(int(total_money)*100)
		wx_order=UnifiedOrder_pub()
		out_trade_no = gen_trade_no()
		wx_order.setParameter("out_trade_no", out_trade_no)
		wx_order.setParameter("body", order_detail)
		wx_order.setParameter('total_fee', '1')
		wx_order.setParameter('openid', openid)
		wx_order.setParameter('spbill_create_ip', request.META['REMOTE_ADDR'])
		prepay_id=wx_order.getPrepayId()	
		response = dict(status=0, pay_type=0, money=total_money)
		
		request.session['prepay_id'] = prepay_id
		#创建一条充值记录
		consumer_order = json.dumps(data)
		recharge = Recharge.objects.create(prepay_id=prepay_id, recharge_person=consumer, out_trade_no=out_trade_no, recharge_value=float(total_money), consumer_order=consumer_order)
		
	return json.dumps(response)

def action_order_query(out_trade_no):
	order_query = OrderQuery_pub()	
	order_query.setParameter('out_trade_no', out_trade_no)
	order_query.getResult()
	return order_query
	
def action_weixin_pay(data, request):
	response = {}
	try:
		print("== prepay_id: %s =="%(data['prepay_id']))
		prepay_id = data['prepay_id']
		recharge = Recharge.objects.filter(prepay_id=prepay_id, status=False)	
		if len(recharge):	
			#主动查询订单
			out_trade_no = recharge[0].out_trade_no				
			order_query = action_order_query(out_trade_no)	
			print("=========trade_state:%s========="%(order_query.result['trade_state']))
			if order_query.result['trade_state'] == SUCCESS:
				consumer_order = request.session['consumer_order']				
				recharge.update(status=True, trade_state=order_query.result['trade_state'], total_fee=order_query.result['total_fee'])
				#支付成功业务
				snd_bonus_pay_weixin(consumer_order)
				
				response = dict(status=SUCCESS, result=SUCCESS)
			else:
				response = dict(status=SUCCESS, result=FAIL)
		else:
			response = dict(status=SUCCESS, result=SUCCESS)
	except:
		log_print(action_weixin_pay)
		response = dict(status=FAIL, err_msg='未知错误')
	return json.dumps(response)
	
#微信支付后发红包
def snd_bonus_pay_weixin(data):
	order_info = decode_order_param(data)
	bonus_info = order_info['bonus_info']
	openid = data['openid']
	consumer = Consumer.objects.get(open_id=openid)
	consumer.snd_person_bonus(bonus_info=bonus_info)
	
	
#ajax请求处理函数
def handle_ajax_request(action, data, request):
	if isinstance(data, (dict,)):
		if action == AJAX_GET_BONUS:
			return action_get_bonus(data['openid'], request)
		elif action == AJAX_CREATE_TICKET:
			#清django session
			if 'openid' in request.session:
				del request.session['openid']
			response = action_create_ticket(data)
			return json.dumps(response)
		elif action == AJAX_WEIXIN_ORDER:
			return action_weixin_order(data, request)
		elif action == AJAX_WEIXIN_PAY:
			return action_weixin_pay(data, request)
		elif action == AJAX_BONUS_MESSAGE:
			return action_bonus_message(data)
		elif action == AJAX_BONUS_REFUSE:
			return action_bonus_refuse(data)
		elif action == AJAX_MODIFY_PHONE:
			return action_modify_phone(data)
		elif action == AJAX_MODIFY_ADDRESS:
			return action_modify_address(data)
		elif action == AJAX_MODIFY_EMAIL:
			return action_modify_email(data)
		elif action == AJAX_MODIFY_NAME:
			return action_modify_name(data)
		elif action == AJAX_MODIFY_SEX:
			return action_modify_sex(data)
	else:
		return "faild"


#生成18位订单号，年月日时分秒+四个字随机数字
def gen_trade_no():
	now = datetime.datetime.now()
	strs = now.strftime('%Y%m%d%H%M%S') 
	chars = "0123456789"
	ran = []
	for x in range(4):
		ran.append(chars[random.randrange(0, len(chars))])	

	return strs+"".join(ran)


