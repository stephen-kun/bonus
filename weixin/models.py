# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import django.utils.timezone as timezone
import string, random
from django.core.exceptions import ObjectDoesNotExist
import json
import datetime
from manager.datatype import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from core.utils.timezone import TIMEZONE_CHOICES
from core.utils.models import AutoSlugField
from django.core.urlresolvers import reverse

COMMON_BONUS = 0
RANDOM_BONUS = 1
SYS_BONUS = 2
#LIST_KEY_ID = u'串串'

#两个字典相加
def union_dict(*objs):
	_keys = set(sum([obj.keys() for obj in objs],[]))
	_total = Dict()
	for _key in _keys:
		_total[_key] = sum([obj.get(_key,0) for obj in objs])
	return _total

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

class _BonusContent():
	def __init__(self, name=None, price=None, unit=None, number=0):
		self.name = name
		self.price = price
		self.unit = unit
		self.number = number
		
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

#将红包分拆
def create_primary_key():
	now = datetime.datetime.now()
	strs = now.strftime('%f') 
	chars = "0123456789"
	ran = []
	for x in range(4):
		ran.append(chars[random.randrange(0, len(chars))])	
	return strs+"".join(ran)

class VirtualMoney(models.Model):
	name = models.CharField(unique=True, max_length=40, default="串串")		#虚拟钱币的名字
	price = models.FloatField(default=1.0)	#虚拟钱币的面值
	unit = models.CharField(max_length=10, default="串")		#单位

	def __unicode__(self):
		return "%s" % (self.name)

#桌台表，维护桌台状态
class DiningTable(models.Model):
	index_table = models.CharField(unique=True, max_length=3)	#桌台编号
	status = models.BooleanField(default=False)			#桌台状态
	seats = models.IntegerField(default=4)					#桌台人数
	is_private = models.BooleanField(default=False)		#是否是包厢

	def __unicode__(self):
		return "table %s"%(self.index_table)


#就餐会话
class DiningSession(models.Model):
	person_num	= models.IntegerField(default=0)							#就餐人数
	begin_time = models.DateTimeField(default=timezone.now) 				#开始就餐时间
	over_time = models.DateTimeField(null=True, blank=True)				#结束就餐时间
	total_money = models.FloatField(default=0.0)							#抢到的红包总额
	total_bonus	= models.IntegerField(default=0)							#抢到的红包总个数
	total_number = models.IntegerField(default=0)							#抢到的串串总个数
	table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)			#就餐桌台

	def __unicode__(self):
		return "Dining Session %s"%(self.table.index_table)
		
	@property
	def update_session_info(self):
		rcv_bonus_list = RcvBonus.objects.filter(session=self, is_refuse=False)
		total_bonus = int(0)
		total_money = float(0)
		total_number = int(0)
		for bonus in rcv_bonus_list:
			total_number += bonus.number
			total_bonus += 1
			total_money += bonus.total_money
		self.total_bonus = total_bonus
		self.total_number = total_number
		self.total_money = total_money
		self.save()
	
	#结束就餐会话
	def close_session(self):
		self.over_time = timezone.now()
		#失效该就餐会话发出的红包，将未抢红包以及婉拒红包返回客户账号
		snd_bonus_list = SndBonus.objects.filter(session=self, is_exhausted=False).update(is_valid=False)
		rcv_bonus_list = RcvBonus.objects.filter(session=self, is_receive=False)
		for bonus in rcv_bonus_list:
			money_list = WalletMoney.objects.filter(rcv_bonus=bonus)
			for money in money_list:
				money.snd_bonus = None
				money.rcv_bonus = None
				money.is_send = False
				money.is_receive = False
				money.ticket = None
				money.save()
		rcv_bonus_list.update(is_valid=False)
		
		#关闭就餐会话，释放桌台
		self.table.status = False
		self.table.save()
		consumer_list = Consumer.objects.filter(session=self)
		for consumer in consumer_list:
			consumer.on_table = None
			consumer.session = None
			consumer.save()
		self.save()

	def create_ticket(self, ticket, total_money):
		ticket_value = float(0)
		if total_money:
			rcv_bonus_list = RcvBonus.objects.filter(session=self, is_refuse=False, is_receive=True)
			sum = float(0)
			for bonus in rcv_bonus_list:
				money_list = WalletMoney.objects.filter(rcv_bonus=bonus)
				for money in money_list:
					sum += money.money.price
					if sum > total_money:
						money.ticket = None
						money.is_send = False
						money.is_receive = False
						money.snd_bonus = None
						money.rcv_bonus = None					
					else:
						ticket_value = sum
						money.ticket = ticket
					money.consumer = ticket.consumer
					money.save()	
		return ticket_value
		
	@property
	def consumers(self):
		return self.consumer_set.all()

	@property
	def consumer_number(self):
		return self.consumer_set.all().count()
		
	def rcv_bonus(self):
		bonus_set = RcvBonus.objects.filter(session=self, is_refuse=False)
		return bonus_set

	def rcv_bonus_contents(self):
		contents = Dict()
		for bonus in self.rcv_bonus():
			contents = union_dict(contents, bonus.good_contents())
		return contents

class ConsumerGifts(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	comment = models.ForeignKey("comment.Comment",related_name='comment_gifts')

#消费者数据表
class Consumer(models.Model):
	open_id = models.CharField(max_length=30,unique=True)  # 微信openId
	user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("profile"), related_name='jf')

	slug = AutoSlugField(populate_from="user.username", db_index=False, blank=True)
	location = models.CharField(_("location"), max_length=75, blank=True)
	last_seen = models.DateTimeField(_("last seen"), auto_now=True)
	last_ip = models.GenericIPAddressField(_("last ip"), blank=True, null=True)
	localtimezone = models.CharField(_("time zone"), max_length=32, choices=TIMEZONE_CHOICES, default='UTC')
	is_administrator = models.BooleanField(_('administrator status'), default=False)
	is_moderator = models.BooleanField(_('moderator status'), default=False)
	is_verified = models.BooleanField(_('verified'), default=False,
									  help_text=_('Designates whether the user has verified his '
												  'account by email or by other means. Un-select this '
												  'to let the user activate his account.'))

	topic_count = models.PositiveIntegerField(_("topic count"), default=0)
	comment_count = models.PositiveIntegerField(_("comment count"), default=0)

	name = models.CharField(max_length=50, default='小明')  # 用户名
	sex = models.CharField(max_length=1, default='0')  # 性别
	phone_num = models.CharField(max_length=20, null=True, blank=True)  # 电话
	address = models.CharField(max_length=30, null=True, blank=True)  # 地址
	picture = models.URLField(null=True, blank=True)  # 头像地址
	bonus_range = models.IntegerField(default=0)  # 排行榜名次
	snd_bonus_num = models.IntegerField(default=0)  # 发串串总数
	rcv_bonus_num = models.IntegerField(default=0)  # 收串串总数
	snd_bonus_value = models.FloatField(default=0)  # 发串串金额
	rcv_bonus_value = models.FloatField(default=0)		#收串串金额
	own_bonus_value = models.FloatField(default=0)  # 可用红包金额
	own_bonus_detail = models.CharField(max_length=300, null=True, blank=True)  # 可用红包明细
	own_ticket_value = models.IntegerField(default=0)  # 可用礼券金额
	create_time = models.DateTimeField(default=timezone.now())  # 首次关注时间
	subscribe = models.BooleanField(default=True)  # 是否关注
	dining_time = models.DateTimeField(default=timezone.now())  # 就餐时间
	on_table = models.ForeignKey(DiningTable, on_delete=models.CASCADE,null=True,blank=True)  # 就餐桌台
	session = models.ForeignKey(DiningSession, null=True, blank=True, related_name="consumer_set", on_delete=models.CASCADE)
	is_admin = models.BooleanField(default=False)
	latest_time = models.DateTimeField(default=timezone.now)		#最近到店时间

	class Meta:
		verbose_name = _("forum profile")
		verbose_name_plural = _("forum profiles")
		
	@property
	def own_money_list(self):
		return WalletMoney.objects.filter(consumer=self, ticket=None, is_used=False, is_valid=True, is_send=False)
		
	@property
	def flush_own_money(self):
		money_list = self.own_money_list
		num = len(money_list)
		sum_money = float(0)
		if num:
			sum_money = money_list[0].money.price * num
		self.own_bonus_value = sum_money
		self.own_bonus_detail = bonus_content_models_to_json(money_list)
		self.save()
		print("===flush_own_money: num: %d price: %f ==="%(num, sum_money))
		
	@property		
	def update_self_info(self):
		snd_bonus_list = SndBonus.objects.filter(consumer=self)
		rcv_bonus_list = RcvBonus.objects.filter(consumer=self, is_refuse=False)
		total_num = 0
		total_money = 0
		for bonus in snd_bonus_list:
			total_num += bonus.number
			total_money += bonus.total_money
		self.snd_bonus_num = total_num
		self.snd_bonus_value = total_money
		total_num = 0
		total_money = 0
		for bonus in rcv_bonus_list:
			total_num += bonus.number
			total_money += bonus.total_money
		self.rcv_bonus_num = total_num
		self.rcv_bonus_value = total_money	
		self.save()
		self.flush_own_money
		
		
	
	@property
	def own_ticket_list(self):
		ticket_list = Ticket.objects.filter(consumer=self, is_valid=True).order_by('create_time').reverse()
		return ticket_list

	def save(self, *args, **kwargs):
		try:
			existing = Consumer.objects.get(user=self.user)
			self.id = existing.id #force update instead of insert
		except Consumer.DoesNotExist:
			pass

		if self.user.is_superuser:
			self.is_administrator = True

		if self.is_administrator:
			self.is_moderator = True

		models.Model.save(self, *args, **kwargs)
		
	#结算
	def close_an_account(self, ticket, ticket_value):
		sum = float(0)
		session_money = self.session.total_money
		total_money = session_money + self.own_bonus_value
		if(ticket_value <= session_money):
			sum = self.session.create_ticket(ticket, ticket_value)
		elif ticket_value <= total_money:
			sum = self.session.create_ticket(ticket, session_money)
			sum = self.wallet_pay_ticket(ticket, (ticket_value - session_money))
			sum += session_money
		else:
			sum = self.session.create_ticket(ticket, session_money)
			sum = self.wallet_pay_ticket(ticket, self.own_bonus_value)	
			sum = total_money
		return sum

	def get_absolute_url(self):
		return reverse('user:detail', kwargs={'pk': self.user.pk, 'slug': self.slug})


	def __unicode__(self):
		return self.name

	@property
	def recharges(self):
		return self.recharge_set.all()

	def account_charge(self, kw):
		total_value=0
		for name,counter in kw.items():
			good=VirtualMoney.objects.get(name=name)
			total_value = total_value + counter*good.price

		recharge_type = 1 if self.is_admin else 0
		charge=Recharge.objects.create(recharge_value=total_value, recharge_type=recharge_type, recharge_person=self )

		for name,counter in kw.items():
			good=VirtualMoney.objects.get(name=name)
			for i in range(counter):
				WalletMoney.objects.create(id_money=create_primary_key(), is_valid=True, consumer=self, recharge=charge, money=good)
			self.change_valid_good(good, 0, counter)

	@property
	def invalid_goods_detail(self):
		return self.consumer_goods.filter(is_valid=False)

	@property
	def valid_goods(self):
		return self.consumer_goods.filter(status=0)

	def get_valid_good_number(self, good):
		account_good, created=self.consumer_goods.get_or_create(is_valid=True, good=good)
		return account_good.number

	def get_valid_good_number_by_name(self, good_name):
		try:
			good = VirtualMoney.objects.get(name=good_name)
		except ObjectDoesNotExist:
			return 0

		account_good, created=self.consumer_goods.get_or_create(status=0, good=good)
		return account_good.number

	def change_valid_good(self, good, status, number):
		account_good, created=self.consumer_goods.get_or_create(status=status, good=good)
		account_good.number += number
		account_good.save()

	@property
	def valid_tickets(self):
		ticket_vn={}
		tickets=self.ticket_set.filter(ticket_type=1,is_consume=False)
		for t in tickets:
			if(ticket_vn.has_key(t.ticket_value)):
				ticket_vn[t.ticket_value] += 1
			else:
				ticket_vn[t.ticket_value] = 1

		return ticket_vn

	def get_wallets_by_good(self, good):
		valid_wallets=self.wallet_set.filter(is_used=False,is_send=False, money=good)
		return valid_wallets
		
	def wallet_pay_ticket(self, ticket, total_money):
		ticket_value = float(0)		
		if total_money:
			sum = float(0)
			money_list = self.own_money_list.order_by("create_time").reverse()
			for money in money_list:
				sum += money.money.price
				if sum > total_money:
					break
				else:
					ticket_value = sum
					money.ticket = ticket
					money.save()
		return ticket_value
	
	def wallet_pay_bonus(self, snd_bonus):
		money_list = self.own_money_list.order_by("create_time").reverse()
		total_money = snd_bonus.total_money
		for money in money_list:
			if total_money:
				money.snd_bonus = snd_bonus
				money.is_send = True
				money.save()
				total_money -= money.money.price
			else:
				break
		
	def snd_person_bonus(self, bonus_info):
		#创建一个红包
		snd_bonus = SndBonus.objects.create(id_bonus=create_primary_key(), consumer=self, bonus_type=bonus_info.bonus_type, to_table=bonus_info.table,\
					to_message=bonus_info.message, content=bonus_info.content, bonus_num=bonus_info.bonus_num, number=bonus_info.number,\
					total_money=bonus_info.money, bonus_remain=bonus_info.bonus_num, session=self.session)
		#将钱装入红包
		self.wallet_pay_bonus(snd_bonus)
		#更新钱包
		self.snd_bonus_num += int(bonus_info.number)
		self.snd_bonus_value +=  float(bonus_info.money)
		self.flush_own_money
		#预分配红包
		snd_bonus.split_to_rcv_bonus(int(bonus_info.number))	


	def send_sys_bonus(self, counter, good_contents, title="趣八八", message=""):
		bonus=SndBonus.objects.create(id_bonus=create_primary_key(), consumer=self, bonus_type=SYS_BONUS, to_message=message, title=title, bonus_num=counter, bonus_remain=counter)
		total_good_num=0
		for name,number in good_contents.items():
			for c in self.valid_goods:
				if(name==c.good.name):
					wallets=self.get_wallets_by_good(c.good)
					for w in wallets[:number]:
						w.snd_bonus=bonus
						w.is_send=True
						w.save()
					self.change_valid_good(c.good, 0, -number)
					self.change_valid_good(c.good, 1, number)
			total_good_num += number

		bonus.split_to_rcv_bonus(total_good_num)


	@property
	def is_seller(self):
		try:
			return Group.objects.get(id=2) in self.user.groups.all()
		except Exception as ex:
			return False

class ConsumerAccountGoods(models.Model):
	good = models.ForeignKey(VirtualMoney, on_delete=models.CASCADE)	#虚拟货币
	consumer = models.ForeignKey(Consumer, null=True,related_name='consumer_goods', on_delete=models.CASCADE)		#就餐的消费者
	number = models.IntegerField(default=0)
	status = models.IntegerField(default=0) #0-idle, 1-fling, 2-used

#Consumer 就餐记录
class ConsumerSession(models.Model):
	session = models.ForeignKey(DiningSession, null=True, on_delete=models.CASCADE)	#就餐会话
	consumer = models.ForeignKey(Consumer, null=True, on_delete=models.CASCADE)		#就餐的消费者
	time = models.DateTimeField(default=timezone.now) 				#记录时间
	

#充值记录
class Recharge(models.Model):
	recharge_value = models.FloatField(default=0.0)			#充值金额
	recharge_time = models.DateTimeField(default=timezone.now)						#充值时间
	recharge_type = models.IntegerField(default=0)				#充值方式：微信/商家系统/买单结余/婉拒/红包未被领取
	recharge_person = models.ForeignKey(Consumer, null=True, related_name='recharge_set', on_delete=models.CASCADE)			#充值人

	prepay_id = models.CharField(unique=True, max_length=64)	#预支付标识
	out_trade_no = models.CharField(unique=True, max_length=18) #商家订单号	
	status = models.BooleanField(default=False)				#订单状态 0:未处理 1:已处理
	trade_state = models.CharField(null=True, blank=True, max_length=32)
	total_fee = models.IntegerField(default=0)				# 1 代表一分钱
	consumer_order = models.CharField(null=True, blank=True, max_length=400)	
	number = models.IntegerField(default=0)					#串串个数

	@property
	def charge_money(self):
		if not self.status:
			money_list = VirtualMoney.objects.all()
			money = money_list[0]
			for x in range(self.number):
				WalletMoney.objects.create(id_money=create_primary_key(),consumer=self.recharge_person, recharge=self, money=money)
			
	def __unicode__(self):
		return '%s Recharge'%(self.recharge_person.name)

	@property
	def consumed_wallets(self):
		return self.wallet_set.filter(is_used=True)

	@property
	def not_consumed_wallets(self):
		return self.wallet_set.filter(is_used=False)

	@property
	def all_wallets(self):
		return self.wallet_set.all()

#消费券
class Ticket(models.Model):
	id_ticket = models.CharField(unique=True, max_length=12)		#消费券唯一id
	title = models.CharField(max_length=100, null=True, blank=True)				#冠名	
	ticket_type = models.IntegerField(default=0)            #消费券类型：0-生成券，1-系统券
	ticket_value = models.FloatField(default=0.0)			#券值
	create_time = models.DateTimeField(default=timezone.now)					#消费券创建时间
	valid_time = models.DateTimeField(null=True, blank=True)					#消费券有效时间
	is_consume = models.BooleanField(default=False)                    #是否被使用
	is_valid = models.BooleanField(default=True)								#是否有效
	consume_time = models.DateTimeField(null=True, blank=True)					#消费使用时间
	consumer = models.ForeignKey(Consumer, null=True,related_name='ticket_set', on_delete=models.CASCADE)	#消费券拥有着

	def __unicode__(self):
		if self.consumer:
			return '%s ticket id %s'%(self.consumer.name, self.id_ticket)
		else:
			return 'ticket id %s'%(self.id_ticket)

#接收红包记录
class RecordRcvBonus(models.Model):
	id_record = models.CharField(unique=True, max_length=12)				#收红包记录的唯一id
	bonus_num = models.IntegerField(default=0)						#收到的红包个数
	record_time = models.DateTimeField(default=timezone.now)		#记录时间
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE) #具体红包

	def __unicode__(self):
		return '%s RecordRcvBonus %s'%(self.consumer.name, self.id_record)
		
class AuthCode(models.Model):
	id_code = models.CharField(unique=True, max_length=6)		#验证码

#发出的红包
class SndBonus(models.Model):
	id_bonus = models.CharField(unique=True, max_length=12)							#个人红包唯一id
	bonus_type = models.IntegerField(default=0)								#红包类型：0:普通红包/1:手气红包/2:系统红包
	to_table = models.CharField(max_length=3,null=True, blank=True)			#收红包的桌台
	to_message = models.CharField(max_length=140, null=True, blank=True)		#赠言
	title = models.CharField(max_length=40, null=True, blank=True)			#冠名
	content = models.CharField(max_length=300, null=True, blank=True)			#红包内容
	bonus_num = models.IntegerField(default=0)				#红包个数
	number = models.IntegerField(default=0)				#串串个数
	total_money = models.FloatField(default=0)				#总金额
	bonus_remain = models.IntegerField(default=0)			#剩余红包个数
	bonus_exhausted = models.IntegerField(default=0)		#已领红包个数
	is_exhausted = models.BooleanField(default=False)		#红包已耗尽
	is_valid = models.BooleanField(default=True)			#红包已失效
	create_time = models.DateTimeField(default=timezone.now)		#发送时间
	over_time = models.DateTimeField(null=True, blank=True)		#抢完时间
	user_time = models.DateTimeField(null=True, blank=True)		#抢完花费时间
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)	#发送红包者
	session = models.ForeignKey(DiningSession, null=True, on_delete=models.CASCADE)	#就餐会话

	def __unicode__(self):
		return '%s SndBonus %s'%(self.consumer.name, self.id_bonus)

	def split_to_rcv_bonus(self, money_num):
		number_list=get_random_bonus(int(money_num), int(self.bonus_num))
		number_list.sort(reverse=True)
		is_best = True
		total_number = 0
		for number in number_list:
			total_money = 0
			rcv_bonus = RcvBonus.objects.create(id_bonus=create_primary_key(), snd_bonus=self, bonus_type = self.bonus_type, session=self.session)
			money_list = WalletMoney.objects.filter(snd_bonus=self, is_receive=False)[0:number]
			account = 0	#统计串串个数
			for money in money_list:
				money.rcv_bonus = rcv_bonus
				money.is_receive = True
				#if money.money.name == LIST_KEY_ID:
				account += 1
				money.save()
				total_money += money.money.price
			rcv_bonus.number = account
			rcv_bonus.total_money = total_money
			if is_best and (rcv_bonus.bonus_type != COMMON_BONUS):
				rcv_bonus.is_best = True
				is_best = False
			rcv_bonus.content=bonus_content_detail(bonus=rcv_bonus, type='rcv')
			rcv_bonus.save()
			total_number += account
		

	def good_contents(self):
		wallets = self.wallet_set.all()
		content = Dict()
		for wallet in wallets:
			if(content.has_key(wallet.money.name)):
				content[wallet.money.name] += 1
			else:
				content[wallet.money.name] = 1
		return content

	def remain_good_contents(self):
		wallets = self.wallet_set.filter(is_receive=False)
		content = Dict()
		for wallet in wallets:
			if (content.has_key(wallet.money.name)):
				content[wallet.money.name] += 1
			else:
				content[wallet.money.name] = 1
		return content




#接收的红包
class RcvBonus(models.Model):
	id_bonus = models.CharField(unique=True, max_length=12)						#收到的红包唯一id
	bonus_type = models.IntegerField(default=0)							#红包类型：0:普通红包/1:手气红包/2:系统红包
	is_message = models.BooleanField(default=False)						#是否已留言
	message = models.CharField(max_length=40, null=True, blank=True)		#留言内容
	is_valid = models.BooleanField(default=True)							#是否有效
	is_receive = models.BooleanField(default=False)						#是否已被领取
	is_refuse = models.BooleanField(default=False)							#是否已拒绝
	content = models.CharField(max_length=300, null=True, blank=True)		#红包内容
	datetime = models.DateTimeField(default=timezone.now)					#接收时间
	number = models.IntegerField(default=0)								#串串个数
	total_money = models.FloatField(default=0)								#总金额
	is_best = models.BooleanField(default=False)							#是否手气最佳
	snd_bonus = models.ForeignKey(SndBonus, on_delete=models.CASCADE)		#红包的唯一id
	consumer = models.ForeignKey(Consumer, null=True, blank=True, on_delete=models.CASCADE)		#消费者的唯一id
	record_rcv_bonus = models.ForeignKey(RecordRcvBonus, null=True, blank=True, on_delete=models.CASCADE)	#抢红包记录
	session = models.ForeignKey(DiningSession, null=True, blank=True, related_name="rcv_bonus_set", on_delete=models.CASCADE)	#就餐会话

	def __unicode__(self):
		if self.consumer:
			return '%s RcvBonus %s'%(self.consumer.name, self.id_bonus)
		else:
			return '未领取 RcvBonus %s'%(self.id_bonus)
	
	#婉拒
	def bonus_refuse(self):
		self.is_refuse = True
		self.is_valid = False
		money_list = WalletMoney.objects.filter(rcv_bonus=self).update(consumer=self.snd_bonus.consumer, is_send=False, is_receive=False, snd_bonus=None, rcv_bonus=None)
		self.consumer.rcv_bonus_num -= self.number
		self.consumer.flush_own_money
		self.save()
		
	
	@property
	def moeny_content(self):
		bonus_content_detail(bonus=self, type='rcv')

	def good_contents(self):
		wallets = self.wallet_set.all()
		content = Dict()
		for wallet in wallets:
			if (content.has_key(wallet.money.name)):
				content[wallet.money.name] += 1
			else:
				content[wallet.money.name] = 1
		return content


# 钱包
class WalletMoney(models.Model):
	id_money = models.CharField(unique=True, max_length=12)				#虚拟钱币的唯一id
	is_valid = models.BooleanField(default=True)					#是否有效
	is_used = models.BooleanField(default=False)					#是否已用
	consumer = models.ForeignKey(Consumer, null=True, related_name="wallet_set", on_delete=models.CASCADE)		#钱包拥有着
	snd_bonus = models.ForeignKey(SndBonus, null=True, related_name="wallet_set", on_delete=models.CASCADE)		#红包唯一id
	is_send = models.BooleanField(default=False)							#是否已发做红包
	ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.CASCADE)			#消费券唯一id
	recharge = models.ForeignKey(Recharge, null=True, related_name='wallet_set', on_delete=models.CASCADE)	#充值记录id
	create_time = models.DateTimeField(default=timezone.now)		#创建时间
	rcv_bonus = models.ForeignKey(RcvBonus, null=True, blank=True, related_name="wallet_set", on_delete=models.CASCADE)		#抢到的红包唯一id
	is_receive = models.BooleanField(default=False)						#是否已接收红包
	money = models.ForeignKey(VirtualMoney, on_delete=models.CASCADE)	#虚拟货币

	def __unicode__(self):
		if self.consumer:
			return '%s WalletMoney %s'%(self.consumer.name, self.id_money)
		else:
			return 'WalletMoney %s'%(self.id_money)

