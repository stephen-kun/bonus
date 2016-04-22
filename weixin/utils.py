# -*- coding: utf-8 -*-
# utils.py
# Create your utils here.
import random, string
from django.core.exceptions import ObjectDoesNotExist 
from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import Dining,Ticket, RcvBonus, BonusMessage,SndBonus,Recharge, RecordRcvBonus

import json
import pytz
from django.utils import timezone

COMMON_BONUS = "普通红包"	
RANDOM_BONUS = "手气红包"	
SYS_BONUS	= "系统红包"	

AJAX_GET_BONUS = 'ajax_get_bonus'

'''
global null_dining_table
global null_consumer
global admin_consumer
global null_recharge
global null_ticket
global null_rcv_bonus
global null_snd_bonus

null_dining_table = 1
null_consumer = 1
admin_consumer = 1
null_ticket = 1
null_rcv_bonus = 1
null_snd_bonus = 1
null_recharge = 1 

table = DiningTable.objects.get_or_create(index_table='0')
null_dining_table=table[0]

consumer = Consumer.objects.get_or_create(open_id='2000000000', name='null', on_table=null_dining_table)
null_consumer=consumer[0]

consumer = Consumer.objects.get_or_create(open_id='3000000000', name='admin', on_table=null_dining_table)
admin_consumer=consumer[0]

recharge = Recharge.objects.get_or_create(id_recharge=2000000000, recharge_person=null_consumer)
null_recharge=system_recharge[0]

ticket = Ticket.objects.get_or_create(id_ticket=2000000000, consumer=null_consumer)
null_ticket=ticket[0]

snd_bonus = SndBonus.objects.get_or_create(id_bonus=2000000000, consumer=null_consumer, is_exhausted=True)
null_snd_bonus=snd_bonus[0]

rcv_bonus = RcvBonus.objects.get_or_create(id_bonus=2000000000, snd_bonus=null_snd_bonus, consumer=null_consumer, table=null_dining_table)
null_rcv_bonus=rcv_bonus[0]
'''

class GetedBonus():
	def __init__(self, rcv_bonus):
		self.id_bonus = rcv_bonus.id_bonus
		self.openid = rcv_bonus.consumer.open_id
		self.name = rcv_bonus.consumer.name
		self.picture = rcv_bonus.consumer.picture
		self.message = rcv_bonus.snd_bonus.to_message
		self.datetime = rcv_bonus.datetime
		self.title = rcv_bonus.snd_bonus.title
		self.content = json.loads(rcv_bonus.content)


#检测用户是否在就餐状态
def is_consumer_dining(openid):
	consumer = Consumer.objects.get(open_id=openid)
	return consumer.on_table.status
	
	
#主键生成方法
def create_primary_key(key='1', length=9):
    a = list(string.digits)
    random.shuffle(a)   
    primary = key + ''.join(a[:length])
    return string.atoi(primary, 10)

#红包留言
def action_bonus_message(request):
	#从request中解析出openid,rcv_bonus_id,message
	#在BonusMessage表中创建一条记录
	#修改RcvBonus表中is_message==True
	pass
	
#红包婉拒
def action_bonus_refuse(request):
	#从request中解析出openid,rcv_bonus_id
	#根据rcv_bonus_id在表PersonMoney中找到婉拒的id_money。
	#在PersonRecharge表中创建一条记录
	pass

#微信支付
def action_weixin_pay(request):
	#支付成功，在PersonRecharge表中创建一条新纪录
	#在PersonMoney表中创建相应的记录
	#支付失败，在PersonBonus表删除一条openid的最新的记录
	pass
	
#创建消费券事件
def action_create_ticket(request):
	#从request中解析出openid
	#在Ticket表中创建一条新的记录
	#更新SystemMoney表中ticket字段
	#更新PersonMoney表中ticket字段
	pass
	
#生成红包内容字符串
def bonus_content_str(bonus, type='rcv'):
	'''
	type : snd 表示发送的红包，rcv 表示接收的红包
	'''
	if type == 'snd':
		wallet_money = WalletMoney.objects.filter(snd_bonus=bonus)
	elif type == 'rcv':
		wallet_money = WalletMoney.objects.filter(rcv_bonus=bonus)
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
	bonus_type: 普通红包， 手气红包， 系统红包
	'''
	bonus_list = []	
	try:
		record_rcv_bonus = RecordRcvBonus.objects.get(id_record=id_record)
		rcv_bonus = RcvBonus.objects.filter(bonus_type=bonus_type, record_rcv_bonus=record_rcv_bonus)
		for bonus in rcv_bonus:
			geted_bonus = GetedBonus(rcv_bonus=bonus)
			bonus_list.append(geted_bonus)	
	except ObjectDoesNotExist:
		pass
	return bonus_list
	
#抢红包事件
def action_get_bonus(openid):
	#返回抢到的红包个数
	bonus_num = 0	#统计抢到的红包个数
	consumer = Consumer.objects.get(open_id=openid)
	snd_bonus = SndBonus.objects.filter(is_exhausted=False)
	primary_key = create_primary_key()		
	if len(snd_bonus):
		# 创建一条抢红包记录
		record_rcv_bonus = RecordRcvBonus.objects.create(id_record=primary_key, consumer=consumer)
		for bonus in snd_bonus:
			rcv_bonus = RcvBonus.objects.filter(consumer=consumer,snd_bonus=bonus)
			if len(rcv_bonus) == 0:
				if (bonus.bonus_type == COMMON_BONUS) and (bonus.to_table != consumer.on_table.index_table):
					continue
				key = create_primary_key()	
				new_rcv_bonus = RcvBonus.objects.create(id_bonus=key, snd_bonus=bonus, consumer=consumer, table=consumer.on_table, record_rcv_bonus=record_rcv_bonus)													
				money = WalletMoney.objects.filter(bonus=bonus, is_receive=False)

				print('===money:%d  remain:%d==\n'%(len(money), bonus.bonus_remain))
				if bonus.bonus_remain == 1:
					get_num = len(money)
				else:
					num = len(money) - bonus.bonus_remain + 1
					get_num = random.randint(1, num)	
				print('****get_num:%d***\n'%(get_num))
				for i in range(0, get_num):
					money[i].rcv_bonus = new_rcv_bonus
					money[i].is_receive = True
					money[i].consumer = consumer
					money[i].save()	
				bonus_num +=1
				bonus.bonus_remain -= 1
				if bonus.bonus_remain == 0:
					bonus.is_exhausted = True
				bonus.save()
				new_rcv_bonus.content = bonus_content_str(bonus=new_rcv_bonus)
				new_rcv_bonus.save()
		record_rcv_bonus.bonus_num = bonus_num
		record_rcv_bonus.save()
	response = dict(number=bonus_num, id_record=primary_key)
	return json.dumps(response)
	
#发普通红包事件
def action_set_common_bonus(request):
	#在PersonBonus表中创建一条记录
	#查询Consumer表中own_bonus_detail字段，判断是否需要微信支付
	#如果需要微信支付，计算出需要支付的金额，然后调用微信支付
	pass


#发手气红包事件
def action_set_random_bonus(request):
	#在PersonBonus表中创建一条记录
	#查询Consumer表中own_bonus_detail字段，判断是否需要微信支付
	#如果需要微信支付，计算出需要支付的金额，然后调用微信支付	
	pass

#发系统红包事件
def action_set_system_bonus(request):
	#查询settings.AUTH_USER_MODEL表中own_bonus_detail字段，判断是否需有足够的虚拟钱币
	#如果有足够的虚拟钱币，则在SystemBonus表中创建一条记录，否则提示今日系统红包已派完。
	#更新SystemMoney表中bonus字段值
	pass
	
#ajax请求处理函数
def handle_ajax_request(openid, action):
	if action == AJAX_GET_BONUS:
		return action_get_bonus(openid)
	pass
	
