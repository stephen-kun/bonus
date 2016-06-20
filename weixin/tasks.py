# -*- coding: utf-8 -*-
# tasks.py
# Create your tasks here.
from __future__ import absolute_import

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from bonus.celery import app
import datetime
import django.utils.timezone as timezone
from weixin.models import WalletMoney,RcvBonus, SndBonus, Ticket,Consumer, Recharge, DiningSession, log_print

from manager.utils import save_today_daily_detail

@app.task
def task_save_daily_record():
	try:
		save_today_daily_statistics()
	except:
		log_print('save_today_daily_detail')

@app.task
def task_charge_money(charge):
	try:
		charge.charge_money
	except:
		log_print('charge_money')

@app.task
def task_snd_person_bonus(consumer, bonus_info):
	try:
		consumer.snd_person_bonus(bonus_info=bonus_info)
	except:
		log_print('snd_person_bonus')
		
@app.task
def task_charge_and_snd_bonus(recharge, bonus_info):
	try:
		recharge.charge_money
		recharge.recharge_person.snd_person_bonus(bonus_info)	
	except:
		log_print('task_charge_and_snd_bonus')	
	
@app.task
def task_create_ticket(consumer, ticket):
	try:
		#结算操作
		ticket_value = consumer.close_an_account(ticket)
		if ticket_value != ticket.ticket_value:
			WalletMoney.objects.select_for_update().filter(ticket=ticket).update(ticket=None, is_send=False, is_receive=False, snd_bonus=None, rcv_bonus=None)
			Ticket.objects.filter(id=ticket.id).delete()
		#关闭就餐会话
		consumer.session.close_session()
	except:
		log_print('task_create_ticket')
		
@app.task
def task_flush_bonus_list(openid):
	try:
		bonus_range = 1		
		oneself = None		
		length = Consumer.objects.filter(user__groups__name='consumer').count()
		consumer_list = Consumer.objects.filter(user__groups__name='consumer').order_by("rcv_bonus_num").reverse()
		for consumer in consumer_list:
			consumer.bonus_range = bonus_range
			bonus_range += 1
			if consumer.open_id == openid:
				oneself = consumer			
			#consumer.save()	
		if length > 50:
			consumer_list = consumer_list[0:50]	
		return consumer_list, oneself
	except:
		log_print('task_flush_bonus_list')
		return None
		
@app.task
def task_flush_snd_bonus_list(openid):
	try:
		bonus_range = 1		
		oneself = None
		length = Consumer.objects.filter(user__groups__name='consumer').count()		
		consumer_list = Consumer.objects.filter(user__groups__name='consumer').order_by("snd_bonus_num").reverse()
		for consumer in consumer_list:
			consumer.snd_range = bonus_range
			bonus_range += 1
			if consumer.open_id == openid:
				oneself = consumer
			#consumer.save()	
		if length > 50:
			consumer_list = consumer_list[0:50]				
		return consumer_list, oneself
	except:
		log_print('task_flush_snd_bonus_list')	
		return None
		
@app.task		
def periodic_task_ticket_valid():
	valid_time = datetime.datetime.now()
	Ticket.objects.select_for_update().filter(valid_time__lt=valid_time).update(is_valid=False)
	
@app.task
def periodic_task_money_valid():
	valid_time = datetime.datetime.now()
	WalletMoney.objects.select_for_update().filter(valid_time__lt=valid_time).update(is_valid=False)

@app.task
def periodic_task_bonus_valid():
	#将所有未抢红包退回原有用户
	snd_bonus_list = SndBonus.objects.filter(is_valid=True)
	for snd_bonus in snd_bonus_list:
		WalletMoney.objects.select_for_update().filter(snd_bonus=snd_bonus).update(is_send=False, snd_bonus=None, is_receive=False)
		RcvBonus.objects.select_for_update().filter(snd_bonus=snd_bonus, is_receive=False).update(is_valid=False)
	#失效所有未抢红包
	snd_bonus_list = SndBonus.objects.select_for_update().filter(is_valid=True).update(is_valid=False)
	
@app.task
def periodic_task_session_valid():
	session_list = DiningSession.objects.filter(over_time=None)
	for session in session_list:
		session.table.status=False
		session.table.save()
		rcv_list = RcvBonus.objects.filter(session=session)
		for rcv_bonus in rcv_list:
			WalletMoney.objects.select_for_update().filter(rcv_bonus=rcv_bonus).update(consumer=rcv_bonus.consumer, is_send=False, is_receive=False, snd_bonus=None, rcv_bonus=None)
		Consumer.objects.select_for_update().filter(session=session).update(session=None, on_table=None)
	DiningSession.objects.select_for_update().filter(over_time=None).update(over_time=timezone.now())
	
@app.task
def periodic_task_flush_wallet():
	consumer_list = Consumer.objects.filter(user__groups__name='consumer')
	for consumer in consumer_list:
		consumer.flush_own_money
		
		

	
