# -*-utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class Admin_bonus(models.Model):
    create_time = models.DateTimeField()
    valid_time = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL[0])

    def __unicode__(self):
            return "admin bonus"

class Good(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(default=0.0)
    deductible = models.BooleanField(default=True)

    def __unicode__(self):
            return self.name

class Bonus_content(models.Model):
    admin_bonus = models.ForeignKey(Admin_bonus)
    good = models.ForeignKey(Good)
    quantity = models.IntegerField(default=0)
    left_quantity = models.IntegerField(default=0)

class Consumer(models.Model):
    openId = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    sex = models.BooleanField(default=True)
    phoneNum = models.CharField(max_length=20)
    idVIP = models.CharField(max_length=20)
    isdining = models.BooleanField(default=False)

    def __unicode__(self):
            return self.name

class DiningTable(models.Model):
    indexTable = models.IntegerField(primary_key=True)
    status = models.BooleanField()
    seats = models.IntegerField()
    isPrivate = models.BooleanField()
    isSync = models.BooleanField()

    def __unicode__(self):
            return "table %d"%(self.indexTable)

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



