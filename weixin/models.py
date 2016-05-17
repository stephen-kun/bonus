# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import django.utils.timezone as timezone
import string, random
from django.core.exceptions import ObjectDoesNotExist
import json

COMMON_BONUS = 0
RANDOM_BONUS = 1
SYS_BONUS = 2
LIST_KEY_ID = u'串串'

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
def create_primary_key(length=10):
    a = list(string.digits)
    random.shuffle(a)
    primary = ''.join(a[:length])
    return primary

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
    def consumers(self):
        return self.consumer_set.all()

    @property
    def consumer_number(self):
        return self.consumer_set.all().count()

#消费者数据表
class Consumer(models.Model):
    open_id = models.CharField(max_length=30, unique=True)	#微信openId
    is_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=30, default='小明')							#用户名
    sex = models.CharField(max_length=1, default='0')						#性别
    phone_num = models.CharField(max_length=20, null=True, blank=True)		#电话
    address = models.CharField(max_length=30, null=True, blank=True)			#地址
    email = models.EmailField(null=True, blank=True)							#邮箱
    picture = models.URLField(null=True, blank=True)							#头像地址
    bonus_range = models.IntegerField(default=0)					#排行榜名次
    snd_bonus_num = models.IntegerField(default=0)					#发红包总数
    rcv_bonus_num = models.IntegerField(default=0)					#收红包总数
    snd_bonus_value = models.IntegerField(default=0)				#发红包金额
    own_bonus_value = models.IntegerField(default=0)				#可用红包金额
    own_bonus_detail = models.CharField(max_length=300, null=True, blank=True)	#可用红包明细
    own_ticket_num = models.IntegerField(default=0)				#可用券数量
    own_ticket_value = models.IntegerField(default=0)				#可用礼券金额
    create_time = models.DateTimeField(default=timezone.now)		#首次关注时间
    subscribe = models.BooleanField(default=True)					#是否关注
    on_table = models.ForeignKey(DiningTable, null=True, blank=True, on_delete=models.CASCADE)	#就餐桌台
    session = models.ForeignKey(DiningSession, null=True, blank=True, related_name="consumer_set", on_delete=models.CASCADE)	#就餐会话
    latest_time = models.DateTimeField(default=timezone.now)		#最近到店时间

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

    def send_sys_bonus(self, counter, good_contents, title="", message=""):
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
	title = models.CharField(null=True, blank=True)				#冠名
    ticket_type = models.IntegerField(default=0)            #消费券类型：0-生成券，1-系统券
    ticket_value = models.FloatField(default=0.0)			#券值
    create_time = models.DateTimeField(default=timezone.now)					#消费券创建时间
    valid_time = models.DateTimeField(null=True, blank=True)					#消费券有效时间
    is_consume = models.BooleanField(default=False)                             #是否被使用
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
        number_list=get_random_bonus(money_num, self.bonus_num)
        number_list.sort(reverse=True)
        is_best = True
        total_number = 0
        for number in number_list:
            total_money = 0
            rcv_bonus = RcvBonus.objects.create(id_bonus=create_primary_key(), snd_bonus=self)
            money_list = WalletMoney.objects.filter(snd_bonus=self, is_receive=False)[0:number]
            account = 0	#统计串串个数
            for money in money_list:
                money.rcv_bonus = rcv_bonus
                money.is_receive = True
                if money.money.name == LIST_KEY_ID:
                    account += 1
                money.save()
                total_money += money.money.price
            rcv_bonus.bonus_type = self.bonus_type
            rcv_bonus.number = account
            rcv_bonus.total_money = total_money
            if is_best and (rcv_bonus.bonus_type != COMMON_BONUS):
                rcv_bonus.is_best = True
                is_best = False
            rcv_bonus.content=bonus_content_detail(bonus=rcv_bonus, type='rcv')
            rcv_bonus.save()
            total_number += account


#接收的红包
class RcvBonus(models.Model):
    id_bonus = models.CharField(unique=True, max_length=12)						#收到的红包唯一id
    bonus_type = models.IntegerField(default=0)							#红包类型：0:普通红包/1:手气红包/2:系统红包
    is_message = models.BooleanField(default=False)						#是否已留言
    message = models.CharField(max_length=40, null=True, blank=True)		#留言内容
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
    session = models.ForeignKey(DiningSession, null=True, blank=True, on_delete=models.CASCADE)	#就餐会话

    def __unicode__(self):
        if self.consumer:
            return '%s RcvBonus %s'%(self.consumer.name, self.id_bonus)
        else:
            return '未领取 RcvBonus %s'%(self.id_bonus)

    @property
    def moeny_content(self):
        bonus_content_detail(bonus=self, type='rcv')







# 钱包
class WalletMoney(models.Model):
    id_money = models.CharField(unique=True, max_length=12)				#虚拟钱币的唯一id
    is_valid = models.BooleanField(default=True)					#是否有效
    is_used = models.BooleanField(default=False)					#是否已用
    consumer = models.ForeignKey(Consumer, null=True, related_name="wallet_set", on_delete=models.CASCADE)		#钱包拥有着
    snd_bonus = models.ForeignKey(SndBonus, null=True, on_delete=models.CASCADE)		#红包唯一id
    is_send = models.BooleanField(default=False)							#是否已发做红包
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.CASCADE)			#消费券唯一id
    recharge = models.ForeignKey(Recharge, null=True, related_name='wallet_set', on_delete=models.CASCADE)	#充值记录id
    rcv_bonus = models.ForeignKey(RcvBonus, null=True, blank=True, related_name="wallet_set", on_delete=models.CASCADE)		#抢到的红包唯一id
    is_receive = models.BooleanField(default=False)						#是否已接收红包
    money = models.ForeignKey(VirtualMoney, on_delete=models.CASCADE)	#虚拟货币

    def __unicode__(self):
        if self.consumer:
            return '%s WalletMoney %s'%(self.consumer.name, self.id_money)
        else:
            return 'WalletMoney %s'%(self.id_money)

