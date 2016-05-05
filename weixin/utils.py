# -*- coding: utf-8 -*-
# utils.py
# Create your utils here.
import random, string
from django.core.exceptions import ObjectDoesNotExist 
from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus

import urllib2
import json
import pytz
from django.utils import timezone

COMMON_BONUS = 0
RANDOM_BONUS = 1	
SYS_BONUS	= 2	

WEIXIN_PAY = '0'
WALLET_PAY = '1'


AJAX_GET_BONUS = 'ajax_get_bonus'
AJAX_CREATE_TICKET = 'ajax_create_ticket'
AJAX_WEIXIN_PAY = 'ajax_weixin_pay'
AJAX_BONUS_REFUSE = 'ajax_bonus_refuse'
AJAX_BONUS_MESSAGE = 'ajax_bonus_message'

AUTH_CODE = '888888'
LIST_KEY_ID	= '串串'



class _GetedBonus():
	def __init__(self, rcv_bonus):
		self.id_bonus = rcv_bonus.id_bonus
		self.openid = rcv_bonus.consumer.open_id
		self.name = rcv_bonus.snd_bonus.consumer.name
		self.picture = rcv_bonus.snd_bonus.consumer.picture
		self.message = rcv_bonus.snd_bonus.to_message
		self.datetime = rcv_bonus.datetime
		self.title = rcv_bonus.snd_bonus.title
		self.content = json.loads(rcv_bonus.content)
		
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
	def __init__(self, name=None, price=None, unit=None, number=None):
		self.name = name	
		self.price = price
		self.unit = unit		
		self.number = number
		
#判断用户是否有足够零钱支付红包
def is_enough_pay(consumer, bonus_content):
	if consumer.own_bonus_detail:
		# 后面做数据检测，如有异常，能够自修复
		content = json.loads(consumer.own_bonus_detail)
		for key, value in bonus_content.items():
			if key in content:
				v1 = int(value)
				v2 = int(content[key])
				if v1 > v2:
					return False
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
	code = request.GET.get(u'code')
	url = access_token_url.replace('CODE', code)
	response = urllib2.urlopen(url)
	content = response.read()
	access_token = json.loads(content)	
	return access_token['openid']	


#检测用户是否在就餐状态
def is_consumer_dining(openid):
	try:
		consumer = Consumer.objects.get(open_id=openid)
	except ObjectDoesNotExist:
		return False
	return consumer.on_table.status
	
	
#主键生成方法
def create_primary_key(key='1', length=9):
    a = list(string.digits)
    random.shuffle(a)   
    primary = key + ''.join(a[:length])
    return string.atoi(primary, 10)
	
#统计餐桌抢到的所有红包金额
def count_total_money_on_table(openid):
	consumer = Consumer.objects.get("openid")
	table = consumer.on_table
	consumer_list = Consumer.objects.filter(on_table=table)
	
	
	
#查看抢到的红包
def check_geted_bonus(id_record):
	print('*******check_geted_bonus********')
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
			print('===can not match==\n')
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
	rcv_bonus = RcvBonus.objects.get(id_bonus=id_bonus)
	rcv_bonus.message = message
	rcv_bonus.is_message = True
	rcv_bonus.save()
	return ""
	
#红包婉拒
def action_bonus_refuse(request):
	#从request中解析出openid,rcv_bonus_id
	#根据rcv_bonus_id在表PersonMoney中找到婉拒的id_money。
	#在PersonRecharge表中创建一条记录
	pass

#微信支付
def action_weixin_pay(data, session):
	if data["method"] == WEIXIN_PAY:
		#创建一条充值记录
		recharge = Recharge.objects.create(id_recharge=create_primary_key())
		recharge.recharge_value = float(data['money'])
		recharge.recharge_type = int(WEIXIN_PAY)
		openid = data['openid']
		consumer = Consumer.objects.get(open_id=openid)
		recharge.recharge_person = consumer
		
		#创建一条发红包记录
		new_snd_bonus = SndBonus.objects.create(id_bonus=create_primary_key(), consumer=consumer, session=consumer.session)
		bonus = snd_bonus_from_session(session)
		new_snd_bonus.to_message = bonus.message
		new_snd_bonus.to_table = bonus.table
		new_snd_bonus.bonus_type = int(bonus.bonus_type)
		new_snd_bonus.number = bonus.number
		new_snd_bonus.total_money = bonus.money
		if new_snd_bonus.bonus_type == COMMON_BONUS:
			new_snd_bonus.bonus_num = consumer.session.person_num
		else:
			new_snd_bonus.bonus_num = int(bonus.bonus_num)
		new_snd_bonus.bonus_remain = new_snd_bonus.bonus_num

		
		#生成虚拟货币
		money_list = VirtualMoney.objects.all()
		for money in money_list:
			content = bonus.content[money.name]
			content = json.loads(content)
			number = content['number']
			create_vitural_money(consumer, new_snd_bonus, recharge, money, number)
		recharge.save()
		new_snd_bonus.save()		
		#随机分配红包	
	else:
		pass
	return 'pay suc!'
	
#创建消费券事件
def action_create_ticket(data):
	#从request中解析出openid
	#在Ticket表中创建一条新的记录
	#更新SystemMoney表中ticket字段
	#更新PersonMoney表中ticket字段
	src_keys = ['openid', 'person_wallet', 'total_money','ticket_value', 'auth_code']
	if check_ajax_params(src_keys, data):
		openid = data['openid']
		person_wallet = data['person_wallet']
		total_money = data['total_money']
		ticket_value = data['ticket_value']
		auth_code = data['auth_code']
		if auth_code != AUTH_CODE:
			return dict(status=2, error_message="验证码错误，请重新输入！")
		#生成一条消费券记录
		new_ticket = Ticket.objects.create(id_ticket=create_primary_key(), ticket_value=float(ticket_value), valid_time=timezone.now)
		consumer = Consumer.objects.get(open_id=openid)
		new_ticket.consumer = consumer
		new_ticket.save()
		#判断是否有结余
		if float(total_money) <= float(ticket_value):
			pass
		else:
			pass
		
		return dict(status=0, part1=1234, part2=2345, part3=4567)
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
		content = dict(name=money.name, price=money.price, unit=money.unit)
		content = json.dumps(content)
		l_content.append(content)
	request.session['create_bonus'] = dict(zip(l_name, l_content))
	return dict(zip(l_name, l_money))
		
#创建红包内容的字典
def create_bonus_dict(request):
	if "create_bonus" in request.session:
		print("***session create_bonus****")
		return create_bonus_session_to_dict(request)
	else:
		return create_bonus_dict_to_session(request)
	
#我的钱包内容字符串
def decode_bonus_detail(consumer):
	bonus_detail = consumer.own_bonus_detail
	if bonus_detail:
		return json.loads(bonus_detail)
	else:
		return ''
	

#生成红包内容字符串
def bonus_content_str(bonus, type='rcv', consumer=None, is_valid=True):
	'''
	type : snd 表示发送的红包，rcv 表示接收的红包, own 表示拥有的红包
	'''
	if type == 'snd':
		wallet_money = WalletMoney.objects.filter(snd_bonus=bonus)
	elif type == 'rcv':
		wallet_money = WalletMoney.objects.filter(rcv_bonus=bonus)
	elif type == 'own':
		wallet_money = WalletMoney.objects.filter(consumer=consumer, is_valid=is_valid)
	virtual_money = VirtualMoney.objects.all()
	l_name = []
	l_unit = []
	for money in virtual_money:
		l_name.append(money.name)
		l_unit.append(money.unit)
	content_dir = dict(zip(l_name, l_unit))
	temp_dir = content_dir.copy()
	for x in wallet_money:
		temp_dir[x.money.name] += "*"
	for key, value in temp_dir.iteritems():
		v = value.count("*")
		content_dir[key] = '{0}{1}'.format(v, content_dir[key]) 
	return json.dumps(content_dir)

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
	
#抢红包事件
def action_get_bonus(openid):
	#返回抢到的红包个数
	bonus_num = 0	#统计抢到的红包个数
	number = 0		#统计串串个数
	total_money = 0 #统计抢到的红包总额
	consumer = Consumer.objects.get(open_id=openid)
	session = consumer.session							#就餐会话
	snd_bonus_list = SndBonus.objects.filter(is_exhausted=False, is_valid=True)
	primary_key = create_primary_key()		
	if len(snd_bonus_list):
		# 创建一条抢红包记录
		record_rcv_bonus = RecordRcvBonus.objects.create(id_record=primary_key, consumer=consumer)
		for bonus in snd_bonus_list:
			rcv_bonus_list = RcvBonus.objects.filter(consumer=consumer,snd_bonus=bonus)
			if len(rcv_bonus_list) == 0:
				if (bonus.bonus_type == COMMON_BONUS) and (bonus.to_table != consumer.on_table.index_table):
					continue
				new_rcv_bonus = RcvBonus.objects.create(id_bonus=create_primary_key(), snd_bonus=bonus, consumer=consumer, table=consumer.on_table, record_rcv_bonus=record_rcv_bonus)													
				money_list = WalletMoney.objects.filter(snd_bonus=bonus, is_receive=False)

				print('===money:%d  remain:%d==\n'%(len(money_list), bonus.bonus_remain))
				get_num = 0
				if bonus.bonus_remain == 1:
					get_num = len(money_list)
				else:
					num = len(money_list) - bonus.bonus_remain + 1
					get_num = random.randint(1, num)	
				print('****get_num:%d***\n'%(get_num))
				for i in range(0, get_num):
					if money_list[i].money.name == LIST_KEY_ID:
						number += 1	#统计抢到的串串个数
					money_list[i].rcv_bonus = new_rcv_bonus
					money_list[i].is_receive = True
					money_list[i].consumer = consumer
					money_list[i].save()	
					total_money += money_list[i].money.price
				bonus_num +=1
				bonus.bonus_remain -= 1
				if bonus.bonus_remain == 0:
					bonus.is_exhausted = True
				bonus.save()
				new_rcv_bonus.number = number
				new_rcv_bonus.bonus_type = bonus.bonus_type
				new_rcv_bonus.content = bonus_content_str(bonus=new_rcv_bonus)
				
				#添加就餐会话信息
				new_rcv_bonus.session = session
				session.total_money += total_money
				session.total_bonus += number
				session.save()
				
				new_rcv_bonus.save()
				consumer.rcv_bonus_num += number
				consumer.save()
		record_rcv_bonus.bonus_num = bonus_num
		record_rcv_bonus.save()
	response = dict(number=bonus_num, id_record=primary_key)
	return json.dumps(response)
	
#生成虚拟货币
def create_vitural_money(consumer, snd_bonus, recharge, money, number):
	print("***create_vitural_money %s**"%(number))
	for x in range(int(number)):
		wallet_money = WalletMoney.objects.create(id_money=create_primary_key(), consumer=consumer, recharge=recharge, snd_bonus=snd_bonus, money=money)
		wallet_money.save()
	
#发普通红包事件
def action_set_common_bonus(consumer, data_dir):
	#在PersonBonus表中创建一条记录
	#查询Consumer表中own_bonus_detail字段，判断是否需要微信支付
	#如果需要微信支付，计算出需要支付的金额，然后调用微信支付
	print('***action_set_common_bonus******\n')
	id_bonus = create_primary_key()
	index_table = data_dir['table']
	dining_table = DiningTable.objects.get(index_table=index_table)
	snd_bonus = SndBonus.objects.create(id_bonus=id_bonus, consumer=consumer)
	snd_bonus.bonus_type = data_dir['bonus_type']
	snd_bonus.to_table = index_table
	snd_bonus.to_message = data_dir['message']
	snd_bonus.bonus_num = dining_table.seats
	snd_bonus.bonus_remain = dining_table.seats
	
	vitural_money_list = VirtualMoney.objects.all()
	l_id = []
	l_money = []
	for money in vitural_money_list:
		l_id.append(money.id)
		l_money.append(money)
	money_dir = dict(zip(l_id, l_money))
	
	recharge = Recharge.objects.create(id_recharge=create_primary_key(), recharge_person=consumer)
	total_money = 0
	l_name = []
	l_good = []
	for key, value in data_dir.items():
		if key in money_dir:
			bc = _BonusContent()
			bc.name = money_dir[key].name
			bc.price = money_dir[key].price
			bc.unit = money_dir[key].unit
			bc.number = int(value)
			l_name.append(bc.name)
			l_good.append(bc)
			total_money += bc.number*money_dir[key].price
			#生成虚拟货币
			create_vitural_money(consumer, snd_bonus, recharge, money_dir[key], value)
			if key == LIST_KEY_ID:
				snd_bonus.number = bc.number
				consumer.snd_bonus_num += bc.number
				consumer.save()
	snd_bonus.session = consumer.session
	snd_bonus.save()
	good_dir = dict(zip(l_name, l_good))
	return dict(good_list=good_dir, total_money=total_money, enough_money=False, id_recharge=recharge.id_recharge)
	 

#发手气红包事件
def action_set_random_bonus(consumer, data_dir):
	#在PersonBonus表中创建一条记录
	#查询Consumer表中own_bonus_detail字段，判断是否需要微信支付
	#如果需要微信支付，计算出需要支付的金额，然后调用微信支付	
	print('***action_set_random_bonus******\n')	
	id_bonus = create_primary_key()
	index_table = data_dir['table']
	dining_table = DiningTable.objects.get(index_table=index_table)
	snd_bonus = SndBonus.objects.create(id_bonus=id_bonus, consumer=consumer)
	snd_bonus.bonus_type = data_dir['bonus_type']
	snd_bonus.to_table = index_table
	snd_bonus.to_message = data_dir['message']
	snd_bonus.bonus_num = data_dir['bonus_num']
	snd_bonus.bonus_remain = data_dir['bonus_num']
	vitural_money_list = VirtualMoney.objects.all()
	l_id = []
	l_money = []
	for money in vitural_money_list:
		l_id.append(money.id)
		l_money.append(money)
	money_dir = dict(zip(l_id, l_money))
	
	recharge = Recharge.objects.create(id_recharge=create_primary_key(), recharge_person=consumer)
	total_money = 0
	l_name = []
	l_good = []
	for key, value in data_dir.items():
		if key in money_dir:
			bc = _BonusContent()
			bc.name = money_dir[key].name
			bc.price = money_dir[key].price
			bc.unit = money_dir[key].unit
			bc.number = int(value)
			l_name.append(bc.name)
			l_good.append(bc)
			total_money += bc.number*money_dir[key].price
			#生成虚拟货币
			create_vitural_money(consumer, snd_bonus,recharge, money_dir[key], value)
			if key == LIST_KEY_ID:
				snd_bonus.number = bc.number
				consumer.snd_bonus_num += bc.number
				consumer.save()		
	snd_bonus.session = consumer.session
	snd_bonus.save()
	good_dir = dict(zip(l_name, l_good))
	return dict(good_list=good_dir, total_money=total_money, enough_money=False, id_recharge=recharge.id_recharge)

	
#将发红包内容存入session
def snd_bonus_to_session(request, bonus):
	snd_bonus = dict(bonus_type=bonus.bonus_type, table=bonus.table, message=bonus.message, money=bonus.money, bonus_num=bonus.bonus_num, content=bonus.content, number=bonus.number)
	snd_bonus = json.dumps(snd_bonus)
	request.session['snd_bonus'] = snd_bonus
	
#从session中解析出发红包内容
def snd_bonus_from_session(session):
	bonus = _Bonus()
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
	
	
	
#解析支付请求
def decode_choose_pay(request, data_dir):
	print("****decode_choose_pay  *****")
	result = {}
	total_money = 0
	number = 0				#统计串串个数
	create_bonus = create_bonus_session_to_dict(request)
	bonus = _Bonus()
	for key, value in data_dir.items():
		if key in create_bonus:
			create_bonus[key].number = value
			price = float(create_bonus[key].price)
			num = int(value)
			total_money += price*num
			if key == LIST_KEY_ID:
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
	
#ajax请求处理函数
def handle_ajax_request(action, data, session):
	if isinstance(data, (dict,)):	
		if action == AJAX_GET_BONUS:
			return action_get_bonus(data['openid'])
		elif action == AJAX_CREATE_TICKET:
			response = action_create_ticket(data)
			return json.dumps(response)
		elif action == AJAX_WEIXIN_PAY:
			return action_weixin_pay(data, session)
		elif action == AJAX_BONUS_MESSAGE:
			return action_bonus_message(data)
		elif action == AJAX_BONUS_REFUSE:
			return action_bonus_refuse(data)
	else:
		return "faild"
	
