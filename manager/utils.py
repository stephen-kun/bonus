# -*- coding:utf-8 -*-

from manager.models import *
from  weixin.models import *
import datetime
import time
import django.utils.timezone as timezone

def datetime_offset_by_month(datetime1, n = 1):
 
    # create a shortcut object for one day
	one_day = datetime.timedelta(days = 1)
 
    # first use div and mod to determine year cycle
	q,r = divmod(datetime1.month + n, 12)
 
    # create a datetime2
    # to be the last day of the target month
	datetime2 = datetime.datetime(datetime1.year + q, r + 1, 1) - one_day
 
	if datetime1.month != (datetime1 + one_day).month:
		return datetime2
 
 
	if datetime1.day >= datetime2.day:
		return datetime2
 
	return datetime2.replace(day = datetime1.day)


def get_today_daily_detail(is_admin):
	daily_detail_list = []

	good_list = VirtualMoney.objects.all()
	time=datetime.date.today()
	start_date = datetime.datetime(time.year,time.month,time.day,0,0,0,tzinfo=timezone.get_current_timezone())
	end_date = start_date + datetime.timedelta(1)
	if(is_admin):
		charge_list = Recharge.objects.filter(recharge_time__range=(start_date, end_date), recharge_type=1 )
		source='管理员充值'
	else:
		charge_list = Recharge.objects.filter(recharge_time__range=(start_date, end_date), recharge_type=0 )
		source='自己充值'


	for charge in charge_list:
		daily_detail = DailyDetail(consumer=charge.recharge_person, time=charge.recharge_time, action=1,source=source, \
				value=charge.recharge_value)

		wallet_list=WalletMoney.objects.filter(recharge=charge)
		ddc_content=[]
		for g in good_list:
			content={'name':g.name, 'number':0}
			for w in wallet_list:
				if(w.money==g):
					content['number']=content['number']+1

			number=content['number']
			if(number!=0):
				ddc = DailyDetailContent(good=g, number=number, daily_detail=daily_detail )
				ddc_content.append(ddc)

		daily_detail.content = ddc_content
		daily_detail_list.append(daily_detail)

	ticket_list = Ticket.objects.filter(is_consume=True, ticket_type=0, consume_time__range=(start_date, end_date))
	#ticket_list = Ticket.objects.filter(is_consume=True)
	for ticket in ticket_list:
		wallets=WalletMoney.objects.filter(ticket=ticket)
		wallets_number=0
		content=[]

		for w in wallets:
			if (not is_admin) and w.recharge.recharge_type==0:
					source = u"用户充值"
					wallets_number += 1 
			elif is_admin and w.recharge.recharge_type==1:
					source = u"系统红包"
					wallets_number += 1
		if wallets_number>0:
			daily_detail = DailyDetail(consumer=wallets[0].consumer, time=ticket.consume_time, action=-1,source=source, value=wallets[0].money.price*wallets_number)
			ddc = DailyDetailContent(good=wallets[0].money, number=wallets_number, daily_detail=daily_detail )
			content.append(ddc)
			daily_detail.content=content
			daily_detail_list.append(daily_detail)

	daily_detail_list=sorted(daily_detail_list, key=lambda x: x.time)
	return daily_detail_list

def get_today_statistics_list():
	daily_detail_list = []
	#charge_list = Recharge.objects.filter(recharge_time__day=datetime.date.today().strftime('%d')).order_by('recharge_time')

	good_list = VirtualMoney.objects.all()
	charge_list = Recharge.objects.all()

	total_content_list=[]
	for g in good_list:
		total_content={'name':g.name,'price':g.price, 'charge':0, 'charge_value':0, 'consume':0, 'consume_value':0}
		total_content_list.append(total_content)

	for charge in charge_list:
		if(charge.recharge_type==1):
			source='管理员充值'
		else:
			source='自己充值'

		content_list=[]

		wallet_list=WalletMoney.objects.filter(recharge=charge)
		for g in good_list:
			content={'name':g.name, 'number':0}
			for w in wallet_list:
				if(w.money==g):
					content['number']=content['number']+1
			content_list.append(content)

			for tc in total_content_list:
				if(tc['name']==g.name):
					tc['charge']+=content['number']
					tc['charge_value'] = tc['charge']*g.price

		ds = {'consumer':charge.recharge_person, 'time':charge.recharge_time, 'action':'充值', 'content_list':content_list, 'source':source, 'value':charge.recharge_value}
		daily_detail_list.append(ds)


	#ticket_list = Ticket.objects.filter(is_consume=True, consume_time__day=datetime.date.today().strftime('%d'))
	ticket_list = Ticket.objects.filter(is_consume=True)
	for ticket in ticket_list:
		wallet_list=WalletMoney.objects.filter(ticket=ticket)
		for wallet in wallet_list:
			content=u"1%s%s"%(wallet.money.unit, wallet.money.name)
			source = u"%s的充值"%(wallet.recharge.recharge_person.name)
			ds = {'consumer':wallet.consumer, 'time':ticket.consume_time, 'action':'消耗', 'content':content, 'source':source, 'value':wallet.money.price}

	# sort by time
	daily_detail_list=sorted(daily_detail_list, key=lambda s: time.mktime(s['time'].timetuple()))

	total_account={'name':u'合计', 'charge_value':0, 'consume_value':0, 'balance':0}
	for tc in total_content_list:
		total_account['charge_value'] += tc['charge_value']*tc['price']
		total_account['consume_value'] += tc['consume_value']*tc['price']
		total_account['balance'] = total_account['charge_value'] - total_account['consume_value']

	return daily_detail_list, total_content_list, total_account


def get_daily_detail( time, is_admin ):
	now = datetime.datetime.now()
	if((now-time).days==0):
		return get_today_daily_detail(is_admin)
	else:
		return DailyDetail.objects.filter(time__day=time.day, is_admin=is_admin )


def save_today_daily_detail():
	now = datetime.datetime.now()
	DailyDetail.objects.filter(time__day=now.day).delete()
	daily_detail_list=[]
	daily_detail_list.append(get_today_daily_detail(True))
	daily_detail_list.append(get_today_daily_detail(False))
	for daily_detail in daily_detail_list:
		daily_detail.save()
		for ddc in daily_detail.content:
			ddc.daily_detail=daily_detail
			ddc.save()

def get_today_daily_statistics(is_admin):
	dsr = DailyStatisticsRecord(is_admin=is_admin)
	good_set = VirtualMoney.objects.all()
	dgs_list=[]
	for good in good_set:
		dgs_list.append(DailyGoodStatistics(good=good, charge_number=0, consume_number=0, daily_statistics=dsr ))

	dd=get_today_daily_detail(is_admin)
	charge_value=0
	consume_value = 0
	for d in dd:
		if(d.action==1):
			charge_value += d.value
			for dgs in dgs_list:
				for c in d.content:
					if(dgs.good==c.good):
						dgs.charge_number += c.number

		elif(d.action==-1):
			consume_value += d.value
			for dgs in dgs_list:
				for c in d.content:
					if(dgs.good==c.good):
						dgs.consume_number += c.number

	#for dgs in dgs_list:
	#    dgs.save()
	dsr.content = dgs_list

	dsr.charge_value = charge_value
	dsr.consume_value = consume_value

	return dsr

def save_today_daily_statistics():
	time = datetime.datetime.now()

	start_date = datetime.datetime(time.year,time.month, time.day, 0,0,0, tzinfo=timezone.get_current_timezone())
	end_date = start_date + datetime.timedelta(1)

	DailyStatisticsRecord.objects.filter(time__range=(start_date, end_date)).delete()
	daily_statistics = get_today_daily_statistics(True)
	daily_statistics.save()
	for d in daily_statistics.content:
		d.daily_statistics=daily_statistics
		d.save()

	daily_statistics = get_today_daily_statistics(False)
	daily_statistics.save()
	for d in daily_statistics.content:
		d.daily_statistics=daily_statistics
		d.save()

def get_daily_statistics(time, is_admin):
	now = datetime.datetime.now()
	if((now-time).days==0):
		daily_statistics = get_today_daily_statistics(is_admin)
	else:
		start_date = datetime.datetime(time.year,time.month, time.day, 0,0,0, tzinfo=timezone.get_current_timezone())
		end_date = start_date + datetime.timedelta(1)
		daily_statistics = DailyStatisticsRecord.objects.filter(time__range=(start_date, end_date), is_admin=is_admin)

	return daily_statistics

def get_daily_statistics_set(time, is_admin):
	print time
	start_date = datetime.datetime(time.year,time.month, 1, 0,0,0, tzinfo=timezone.get_current_timezone())
	end_date = datetime_offset_by_month(start_date)
	daily_statistics_set = DailyStatisticsRecord.objects.filter(time__range=(start_date, end_date), is_admin=is_admin)
	return daily_statistics_set
