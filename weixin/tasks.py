# -*- coding: utf-8 -*-
# tasks.py
# Create your tasks here.
from __future__ import absolute_import

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from bonus.celery import app
import errno
from celery.exceptions import Reject

from .models import *

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
def task_create_ticket(consumer, ticket):
	try:
		#�������
		consumer.close_an_account(ticket)
		#�رվͲͻỰ
		consumer.session.close_session()
	except:
		log_print('task_create_ticket')
		

	