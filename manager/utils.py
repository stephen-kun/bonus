# -*- coding:utf-8 -*-

from manager.models import *
from  weixin.models import *
import datetime
import time

def save_daily_detail():
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

        daily_detail = DailyDetail.objects.create(consumer=charge.recharge_person, time=charge.recharge_time, action=u'充值',source=source, value=charge.recharge_value)

        wallet_list=WalletMoney.objects.filter(recharge=charge)
        for g in good_list:
            content={'name':g.name, 'number':0}
            for w in wallet_list:
                if(w.money==g):
                    content['number']=content['number']+1

            number=content['number']
            if(number!=0):
                ddc = DailyDetailContent.objects.create(good=g, number=number, daily_detail=daily_detail )
                ddc.save()

        daily_detail.save()

    #ticket_list = Ticket.objects.filter(is_consume=True, consume_time__day=datetime.date.today().strftime('%d'))
    ticket_list = Ticket.objects.filter(is_consume=True)
    for ticket in ticket_list:
        wallet_list=WalletMoney.objects.filter(ticket=ticket)
        for wallet in wallet_list:
            ddc = DailyDetailContent.objects.create(good=wallet.money, number=1, daily_detail=daily_detail )
            ddc.save()
            source = u"%s的充值"%(wallet.recharge.recharge_person.name)
            daily_detail = DailyDetail.objects.create(consumer=wallet.consumer, time=ticket.consume_time, action=u'消耗',source=source, value=wallet.money.price)
            daily_detail.save()

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


def get_daily_detail():
    daily_detail = DailyDetail.objects.all()
    return daily_detail

def save_daily_statistics():
    dsr = DailyStatisticsRecord.objects.create()
    good_set = VirtualMoney.objects.all()
    dgs_list=[]
    for good in good_set:
        dgs_list.append(DailyGoodStatistics.objects.create(good=good, charge_number=0, consume_number=0, daily_statistics=dsr ))

    dd=DailyDetail.objects.filter(action=u'充值')
    charge_value=0
    for d in dd:
        charge_value += d.value
        ddc = DailyDetailContent.objects.filter(daily_detail=d)
        for dc in ddc:
            for dgs in dgs_list:
                if(dgs.good==dc.good):
                    dgs.charge_number += dc.number

    dd=DailyDetail.objects.filter(action=u'消耗')
    consume_value = 0
    for d in dd:
        consume_value += d.value
        ddc = DailyDetailContent.objects.filter(daily_detail=d)
        for dc in ddc:
            for dgs in dgs_list:
                if(dgs.good==dc.good):
                    dgs.consume_number += dc.number

    for dgs in dgs_list:
        dgs.save()

    dsr.charge_value = charge_value
    dsr.consume_value = consume_value
    dsr.save()

def get_daily_statistics():
    daily_statistics = DailyStatisticsRecord.objects.filter(time__day=datetime.date.today().strftime('%d'))
    return daily_statistics[0] if(len(daily_statistics)>0) else None

def get_daily_statistics_set():
    #daily_statistics_set = DailyStatisticsRecord.objects.filter(time__day=datetime.date.today().strftime('%m'))
    daily_statistics_set = DailyStatisticsRecord.objects.all()
    return daily_statistics_set
