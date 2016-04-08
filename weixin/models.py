# -*-utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class SysBonus(models.Model):
	id_bonus = models.IntegerField(primary_key=True)
	create_time = models.DateTimeField()
	valid_time = models.DateTimeField()
	message = models.CharField(max_length=45)
	title = models.CharField(max_length=20)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL[0])

	def __unicode__(self):
		return "System Bonus"
			
class DiningTable(models.Model):
	index_table = models.IntegerField(primary_key=True)
	status = models.BooleanField()
	seats = models.IntegerField()
	is_private = models.BooleanField()

	def __unicode__(self):
		return "table %d"%(self.indexTable)
		
class Consumer(models.Model):
	open_id = models.CharField(max_length=30, primary_key=True)
	name = models.CharField(max_length=30)
	sex = models.BooleanField(default=True)
	phone_num = models.CharField(max_length=20)
	address = models.CharField(max_length=30)
	is_dining = models.BooleanField(default=False)
	snd_bonus_num = models.IntegerField(default=0)
	rcv_bonus_num = models.IntegerField(default=0)
	snd_bonus_value = models.IntegerField(default=0)
	own_bonus_value = models.IntegerField(default=0)
	own_ticket_value = models.IntegerField(default=0)
	create_time = models.DateTimeField()
	on_table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)
	
	def __unicode__(self):
		return self.name
		
class Dining(models.Model):
	pass
	

class Good(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(default=0.0)
    deductible = models.BooleanField(default=True)

    def __unicode__(self):
            return self.name

class Bonus_content(models.Model):
    admin_bonus = models.ForeignKey(SysBonus)
    good = models.ForeignKey(Good)
    quantity = models.IntegerField(default=0)
    left_quantity = models.IntegerField(default=0)



class ConsumeInfo(models.Model):
    totalPrice = models.IntegerField()
    consumerCount = models.IntegerField()
    startTime = models.DateTimeField()
    finishTime = models.DateTimeField()
    whoPay = models.CharField(max_length=30)
    diningTable = models.OneToOneField(DiningTable, on_delete=models.CASCADE)

    def __unicode__(self):
            return "table %d's ConsumeInfo"%(self.diningTable.indexTable)

class ConsumeRecord(models.Model):
    consumeInfo = models.ForeignKey(ConsumeInfo, on_delete=models.CASCADE)
    consumer = models.OneToOneField(Consumer, on_delete=models.CASCADE)

class Account(models.Model):
    sendBonusSum = models.IntegerField(default=0)
    recvBonusSum = models.IntegerField(default=0)
    totalPrice = models.FloatField(default=0.0)
    user = models.OneToOneField(Consumer, on_delete=models.CASCADE)

class SndBonus(models.Model):
    toUser = models.CharField(max_length=30)
    createTime = models.DateTimeField()
    validTime = models.DateTimeField()
    toMessage = models.CharField(max_length=45)
    fromMessage = models.CharField(max_length=45)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class RcvBonus(models.Model):
    fromUser = models.CharField(max_length=30)
    rcvTime = models.DateTimeField()
    validTime = models.DateTimeField()
    fromMessage = models.CharField(max_length=45)
    toMessage = models.CharField(max_length=45)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    consume = models.ForeignKey(ConsumeInfo, on_delete=models.CASCADE)

class AccountContent(models.Model):
    goodsNum = models.IntegerField()
    createTime = models.DateTimeField()
    validTime = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

class SndBonusContent(models.Model):
    contentNum = models.IntegerField()
    sndPackage = models.ForeignKey(SndBonus, on_delete=models.CASCADE)
    good = models.OneToOneField(Good, on_delete=models.CASCADE)

class RcvBonusContent(models.Model):
    contentNum = models.IntegerField()
    rcvPackage = models.ForeignKey(RcvBonus, on_delete=models.CASCADE)
    good = models.OneToOneField(Good, on_delete=models.CASCADE)



