#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone
from weixin.models import Consumer,VirtualMoney

class DailyDetail(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)					#结束就餐时间
    action = models.CharField(default=u'充值', max_length=16)
    source = models.CharField(default=u'管理员充值', max_length=32)
    value = models.FloatField(default=0)

    @property
    def content(self):
        c_set = self.content_set.all()
        content=""
        for c in c_set:
            content=content+"%dx%s "%(c.number, c.good.name)

        return content

class DailyDetailContent(models.Model):
    good = models.ForeignKey(VirtualMoney, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    daily_detail = models.ForeignKey(DailyDetail, on_delete=models.CASCADE, related_name='content_set')


class DailyStatisticsRecord(models.Model):
    time = models.DateTimeField(default=timezone.now)
    consume_value = models.FloatField(default=0)
    charge_value = models.FloatField(default=0)
    account=models.FloatField(default=0)

    @property
    def balance(self):
        return self.charge_value - self.consume_value

    @property
    def content_set(self):
        return self.content_set.all()

class DailyGoodStatistics(models.Model):
    good = models.ForeignKey(VirtualMoney, on_delete=models.CASCADE)
    action=models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    daily_statistics = models.ForeignKey(DailyStatisticsRecord, on_delete=models.CASCADE, related_name='content_set')

