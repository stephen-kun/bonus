# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import django.utils.timezone as timezone
import string, random
from django.core.exceptions import ObjectDoesNotExist

def create_primary_key(key='1', length=9):
    a = list(string.digits)
    random.shuffle(a)
    primary = key + ''.join(a[:length])
    return string.atoi(primary, 10)

# Create your models here.
# 红包日统计表
class BonusCountDay(models.Model):
	consumer = models.CharField(primary_key=True, max_length=30)	#用户唯一id
	count_num = models.IntegerField(default=0)						#主排行统计数
	other_info = models.CharField(max_length=30, null=True, blank=True)					#其他物品统计数，字符串形式


# 红包月统计表
class BonusCountMonth(models.Model):
	consumer = models.CharField(primary_key=True, max_length=30)	#用户唯一id
	count_num = models.IntegerField(default=0)						#主排行统计数
	other_info = models.CharField(max_length=30, null=True, blank=True)					#其他物品统计数，字符串形式

class VirtualMoney(models.Model):
	id = models.CharField(max_length=10, primary_key=True)					#编号
	name = models.CharField(max_length=40, default="串串")		#虚拟钱币的名字
	price = models.FloatField(default=1.0)	#虚拟钱币的面值
	unit = models.CharField(max_length=10, default="串")		#单位


#桌台表，维护桌台状态
class DiningTable(models.Model):
    index_table = models.CharField(primary_key=True, max_length=3)	#桌台编号
    status = models.BooleanField(default=False)			#桌台状态
    seats = models.IntegerField(default=0)					#桌台人数
    is_private = models.BooleanField(default=False)		#是否是包厢

    def __unicode__(self):
        return "table %s"%(self.index_table)

#就餐会话
class DiningSession(models.Model):
    id_session = models.IntegerField(primary_key=True)						#就餐会话唯一id
    person_num	= models.IntegerField(default=0)							#就餐人数
    begin_time = models.DateTimeField(default=timezone.now) 				#开始就餐时间
    over_time = models.DateTimeField(null=True, blank=True)					#结束就餐时间
    consumers = models.CharField(max_length=200, null=True, blank=True)		#一起就餐的消费者
    snd_bonus = models.TextField(max_length=400,null=True, blank=True)		#所有发送的红包
    rcv_bonus = models.TextField(max_length=400,null=True, blank=True)		#所有接收的红包
    total_money = models.FloatField(default=0.0)							#抢到的红包总额
    total_bonus	= models.IntegerField(default=0)							#抢到的红包总个数
    table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)			#就餐桌台

    def __unicode__(self):
        return "Dining Session %d"%(self.id_session)

#消费者数据表
class Consumer(models.Model):
    open_id = models.CharField(max_length=30, primary_key=True)	#微信openId
    is_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=30, default='小明')							#用户名
    sex = models.CharField(max_length=1, default='0')						#性别
    phone_num = models.CharField(max_length=20, null=True, blank=True)		#电话
    address = models.CharField(max_length=30, null=True, blank=True)			#地址
    picture = models.URLField(max_length=200, null=True, blank=True)			#头像地址
    bonus_range = models.IntegerField(default=0)					#排行榜名次
    snd_bonus_num = models.IntegerField(default=0)					#发红包总数
    rcv_bonus_num = models.IntegerField(default=0)					#收红包总数
    snd_bonus_value = models.IntegerField(default=0)				#发红包金额
    own_bonus_value = models.IntegerField(default=0)				#可用红包金额
    own_bonus_detail = models.CharField(max_length=100, default="123456")				#可用红包明细
    own_ticket_value = models.IntegerField(default=0)				#可用礼券金额
    create_time = models.DateTimeField(default=timezone.now)		#首次关注时间
    subscribe = models.BooleanField(default=True)					#是否关注
    on_table = models.ForeignKey(DiningTable, null=True, on_delete=models.CASCADE)	#就餐桌台
    session = models.ForeignKey(DiningSession, null=True, on_delete=models.CASCADE)	#就餐会话
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
        charge=Recharge.objects.create(id_recharge=create_primary_key(), recharge_value=total_value, recharge_type=recharge_type, recharge_person=self )

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

    def send_bonus(self,counter, good_contents, title="", message=""):
        bonus=SndBonus.objects.create(id_bonus=create_primary_key(), consumer=self, bonus_type=2, to_message=message, title=title, bonus_num=counter, bonus_remain=counter)
        for name,number in good_contents.items():
            for c in self.valid_goods:
                if(name==c.good.name):
                    wallets=self.get_wallets_by_good(c.good)
                    for i in range(number):
                        for w in wallets:
                            w.snd_bonus=bonus
                            w.is_send=True
                            w.save()
                    self.change_valid_good(c.good, 0, -number)
                    self.change_valid_good(c.good, 1, number)

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
    id_recharge = models.IntegerField(primary_key=True)		#充值记录id
    recharge_value = models.FloatField(default=0.0)			#充值金额
    recharge_time = models.DateTimeField(default=timezone.now)						#充值时间
    recharge_type = models.IntegerField(default=0)				#充值方式：微信/商家系统/买单结余/婉拒/红包未被领取
    recharge_person = models.ForeignKey(Consumer, null=True, related_name='recharge_set', on_delete=models.CASCADE)			#充值人

    def __unicode__(self):
        return '%s Recharge %d'%(self.recharge_person.name, self.id_recharge)

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
    id_ticket = models.IntegerField(primary_key=True)		#消费券唯一id
    ticket_type = models.IntegerField(default=0)            #消费券类型：0-生成券，1-系统券
    ticket_value = models.FloatField(default=0.0)			#券值
    create_time = models.DateTimeField(default=timezone.now)					#消费券创建时间
    valid_time = models.DateTimeField(null=True, blank=True)					#消费券有效时间
    is_consume = models.BooleanField(default=False)                             #是否被使用
    consume_time = models.DateTimeField(null=True, blank=True)					#消费使用时间
    consumer = models.ForeignKey(Consumer, null=True,related_name='ticket_set', on_delete=models.CASCADE)	#消费券拥有着

    def __unicode__(self):
        return '%s ticket id%d'%(self.consumer.name, self.id_ticket)

#接收红包记录
class RecordRcvBonus(models.Model):
	id_record = models.IntegerField(primary_key=True)				#收红包记录的唯一id
	bonus_num = models.IntegerField(default=0)						#收到的红包个数
	record_time = models.DateTimeField(default=timezone.now)		#记录时间
	consumer = models.ForeignKey(Consumer, null=True, on_delete=models.CASCADE) #具体红包

	def __unicode__(self):
		return '%s RecordRcvBonus %d'%(self.consumer.name, self.id_record)

#发出的红包
class SndBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)							#个人红包唯一id
	bonus_type = models.IntegerField(default=0)								#红包类型：0:普通红包/1:手气红包/2:系统红包
	to_table = models.CharField(max_length=3,null=True, blank=True)			#收红包的桌台
	to_message = models.CharField(max_length=140, null=True, blank=True)		#赠言
	title = models.CharField(max_length=40, null=True, blank=True)			#冠名
	bonus_num = models.IntegerField(default=0)				#红包个数
	number = models.IntegerField(default=0)				#串串个数
	bonus_remain = models.IntegerField(default=0)			#剩余红包个数
	is_exhausted = models.BooleanField(default=False)		#红包已耗尽
	create_time = models.DateTimeField(default=timezone.now)					#发送时间
	consumer = models.ForeignKey(Consumer, null=True, on_delete=models.CASCADE)	#发送红包者
	session = models.ForeignKey(DiningSession, null=True, on_delete=models.CASCADE)	#就餐会话

	def __unicode__(self):
		return '%s SndBonus %d'%(self.consumer.name, self.id_bonus)

#接收的红包
class RcvBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)						#收到的红包唯一id
	bonus_type = models.IntegerField(default=0)							#红包类型：0:普通红包/1:手气红包/2:系统红包
	is_message = models.BooleanField(default=False)						#是否已留言
	is_refuse = models.BooleanField(default=False)							#是否已拒绝
	content = models.CharField(max_length=100, null=True, blank=True)		#红包内容
	datetime = models.DateTimeField(default=timezone.now)					#接收时间
	number = models.IntegerField(default=0)								#串串个数
	is_best = models.BooleanField(default=False)							#是否手气最佳
	snd_bonus = models.ForeignKey(SndBonus, null=True, on_delete=models.CASCADE)		#红包的唯一id
	consumer = models.ForeignKey(Consumer, null=True, on_delete=models.CASCADE)		#消费者的唯一id
	table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)		#桌台号
	record_rcv_bonus = models.ForeignKey(RecordRcvBonus, null=True, on_delete=models.CASCADE)	#抢红包记录
	session = models.ForeignKey(DiningSession, null=True, on_delete=models.CASCADE)	#就餐会话

	def __unicode__(self):
		return '%s RcvBonus %d'%(self.consumer.name, self.id_bonus)


#红包留言
class BonusMessage(models.Model):
	id_message = models.IntegerField(primary_key=True)						#红包留言唯一id
	message = models.CharField(max_length=140, null=True, blank=True)							#留言内容
	rcv_bonus = models.OneToOneField(RcvBonus, on_delete=models.CASCADE)	#接收的红包唯一id
	consumer = models.ForeignKey(Consumer, null=True, on_delete=models.CASCADE)		#留言者唯一id

	def __unicode__(self):
		return '%s BonusMessage %d'%(self.consumer.name, self.id_message)


#虚拟货币
	def __unicode__(self):
		return self.name

# 钱包
class WalletMoney(models.Model):
	id_money = models.IntegerField(primary_key=True)				#虚拟钱币的唯一id
	is_valid = models.BooleanField(default=False)					#是否有效
	is_used = models.BooleanField(default=False)					#是否已用
	consumer = models.ForeignKey(Consumer, null=True, related_name="wallet_set", on_delete=models.CASCADE)		#钱包拥有着
	snd_bonus = models.ForeignKey(SndBonus, null=True, on_delete=models.CASCADE)		#红包唯一id
	is_send = models.BooleanField(default=False)							#是否已发做红包
	ticket = models.ForeignKey(Ticket, null=True, on_delete=models.CASCADE)			#消费券唯一id
	recharge = models.ForeignKey(Recharge, null=True, related_name='wallet_set', on_delete=models.CASCADE)	#充值记录id
	rcv_bonus = models.ForeignKey(RcvBonus, null=True, on_delete=models.CASCADE)		#抢到的红包唯一id
	is_receive = models.BooleanField(default=False)						#是否已接收红包
	money = models.ForeignKey(VirtualMoney, on_delete=models.CASCADE)	#虚拟货币

	def __unicode__(self):
		return '%s WalletMoney %d'%(self.consumer.name, self.id_money)

