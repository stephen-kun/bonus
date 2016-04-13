# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# 红包日统计表
class BonusCountDay(models.Model):
	consumer = models.CharField(primary_key=True, max_length=30)	#用户唯一id
	count_num = models.IntegerField(default=0)						#主排行统计数
	other_info = models.CharField(max_length=30)					#其他物品统计数，字符串形式


# 红包月统计表
class BonusCountMonth(models.Model):
	consumer = models.CharField(primary_key=True, max_length=30)	#用户唯一id
	count_num = models.IntegerField(default=0)						#主排行统计数
	other_info = models.CharField(max_length=30)					#其他物品统计数，字符串形式
	
	
#桌台表，维护桌台状态		
class DiningTable(models.Model):
	index_table = models.CharField(primary_key=True, max_length=3)	#桌台编号
	status = models.BooleanField(default=False)			#桌台状态
	seats = models.IntegerField(default=0)					#桌台入座人数
	is_private = models.BooleanField(default=False)		#是否是包厢

	def __unicode__(self):
		return "table %d"%(self.indexTable)

#消费者数据表		
class Consumer(models.Model):
	open_id = models.CharField(max_length=30, primary_key=True)	#微信openId
	name = models.CharField(max_length=30)							#用户名
	sex = models.BooleanField(default=True)						#性别
	phone_num = models.CharField(max_length=20)					
	address = models.CharField(max_length=30)
	is_dining = models.BooleanField(default=False)					#是否处于就餐状态
	snd_bonus_num = models.IntegerField(default=0)					#发红包总数
	rcv_bonus_num = models.IntegerField(default=0)					#收红包总数
	snd_bonus_value = models.IntegerField(default=0)				#发红包金额
	own_bonus_value = models.IntegerField(default=0)				#可用红包金额
	own_bonus_detail = models.CharField(max_length=30)				#可用红包明细
	own_ticket_value = models.IntegerField(default=0)				#可用礼券金额
	create_time = models.DateTimeField()							#首次关注时间
	subscribe = models.BooleanField(default=True)					#是否关注
	on_table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)	#就餐桌台
	
	def __unicode__(self):
		return self.name
		
#个人充值
class PersonRecharge(models.Model):
	id_recharge = models.IntegerField(primary_key=True)		#充值记录id
	recharge_value = models.FloatField(default=0.0)			#充值金额
	recharge_time = models.DateTimeField()						#充值时间
	recharge_person = models.CharField(max_length=30)			#充值人
	recharge_type = models.IntegerField(default=0)				#充值方式：微信/买单结余/婉拒/红包未被领取
	
	def __unicode__(self):
		return self.recharge_person
		
#系统充值记录
class SystemRecharge(models.Model):
	id_recharge = models.IntegerField(primary_key=True)		#充值记录id
	recharge_value = models.FloatField(default=0.0)			#充值金额
	recharge_time = models.DateTimeField()						#充值时间
	recharge_person = models.CharField(max_length=30)			#充值人
	
	def __unicode__(self):
		return self.recharge_person

#就餐记录表		
class Dining(models.Model):
	id_table = models.IntegerField()		#桌号
	begin_time = models.DateTimeField() 	#开始就餐时间
	over_time = models.DateTimeField()		#结束就餐时间
	consumer = models.OneToOneField(Consumer, on_delete=models.CASCADE)	#关联消费者
	
	def __unicode__(self):
		return "Dining Record %s"%(self.consumer.name)
		
		
#消费券
class Ticket(models.Model):
	id_ticket = models.IntegerField(primary_key=True)		#消费券唯一id
	ticket_value = models.FloatField(default=0.0)			#券值
	create_time = models.DateTimeField()					#消费券创建时间
	valid_time = models.DateTimeField()					#消费券有效时间
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)	#消费券拥有着
	
#个人的红包
class PersonBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)		#个人红包唯一id
	bonus_type = models.IntegerField(default=0)			#红包类型：普通红包/手气红包/系统红包
	to_table = models.IntegerField()						#收红包的桌台
	from_table = models.IntegerField()						#发红包的桌台
	to_message = models.CharField(max_length=140)			#赠言
	title = models.CharField(max_length=40)				#冠名
	bonus_num = models.IntegerField(default=0)				#红包个数
	bonus_remain = models.IntegerField(default=0)			#剩余红包个数
	is_exhausted = models.BooleanField(default=False)		#红包已耗尽
	create_time = models.DateTimeField()					#发送时间
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)	#发送红包者
	
	def __unicode__(self):
		return self.consume.name
		
#系统红包
class SystemBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)		#系统红包唯一id
	bonus_type = models.IntegerField(default=0)			#红包类型：普通红包/手气红包/系统红包
	to_message = models.CharField(max_length=45)			#赠言
	title = models.CharField(max_length=20)				#冠名
	bonus_num = models.IntegerField(default=0)				#红包个数
	bonus_remain = models.IntegerField(default=0)			#剩余红包个数
	is_exhausted = models.BooleanField(default=False)		#红包已耗尽
	create_time = models.DateTimeField()					#发送时间
	admin = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL[0])	#发送红包者

	def __unicode__(self):
		return "System Bonus"
		
#接收的红包
class RcvBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)						#收到的红包唯一id
	is_message = models.BooleanField(default=False)						#是否已留言
	is_refuse = models.BooleanField(default=False)							#是否能够拒绝
	person_bonus = models.ForeignKey(PersonBonus, on_delete=models.CASCADE)#个人红包的唯一id
	system_bonus = models.ForeignKey(SystemBonus, on_delete=models.CASCADE)#系统红包的唯一id
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)		#消费者的唯一id
	table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)		#桌台号
	
	
#红包留言
class BonusMessage(models.Model):
	id_message = models.IntegerField(primary_key=True)						#红包留言唯一id
	message = models.CharField(max_length=140)								#留言内容
	rcv_bonus = models.OneToOneField(RcvBonus, on_delete=models.CASCADE)	#接收的红包唯一id
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)		#留言者唯一id
	
#虚拟货币
class VirtualMoney(models.Model):
	name = models.CharField(primary_key=True,max_length=40)	#虚拟钱币的名字
	price = models.FloatField(default=0.0)						#虚拟钱币的面值

	def __unicode__(self):
		return self.name
		
#系统虚拟钱币
class SystemMoney(models.Model):
	id_money = models.IntegerField(primary_key=True)				#虚拟钱币的唯一id
	is_valid = models.BooleanField(default=True)					#是否有效
	is_used = models.BooleanField(default=False)					#是否已用
	admin = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL[0])	#钱包拥有者
	bonus = models.ForeignKey(SystemBonus, on_delete=models.CASCADE)		#红包唯一id
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)			#消费券唯一id
	recharge = models.ForeignKey(SystemRecharge, on_delete=models.CASCADE)	#充值记录id
	rcv_bonus = models.ForeignKey(RcvBonus, on_delete=models.CASCADE)		#抢到的红包唯一id
	money = models.OneToOneField(VirtualMoney, on_delete=models.CASCADE)	#虚拟货币
	
#个人虚拟钱币
class PersonMoney(models.Model):
	id_money = models.IntegerField(primary_key=True)				#虚拟钱币的唯一id
	is_valid = models.BooleanField(default=True)					#是否有效
	is_used = models.BooleanField(default=False)					#是否已用
	consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)		#钱包拥有着
	bonus = models.ForeignKey(PersonBonus, on_delete=models.CASCADE)		#红包唯一id
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)			#消费券唯一id
	recharge = models.ForeignKey(PersonRecharge, on_delete=models.CASCADE)	#充值记录id
	rcv_bonus = models.ForeignKey(RcvBonus, on_delete=models.CASCADE)		#抢到的红包唯一id
	money = models.OneToOneField(VirtualMoney, on_delete=models.CASCADE)	#虚拟货币
	
