# -*- coding: utf-8 -*-
# wechat.py
# Create your wechat here.
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages

from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,PersonRecharge,SystemRecharge,VirtualMoney
from .models import Dining,Ticket, PersonBonus, SystemBonus, RcvBonus, BonusMessage, SystemMoney, PersonMoney
from django.core.exceptions import ObjectDoesNotExist 
import pytz
from django.utils import timezone
import re

TOKEN = 'token'
APPID = 'wxc32d7686c0827f2a'
APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URI&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)

global wechat

conf = WechatConf(
    token = TOKEN,
    appid = APPID,
    appsecret = APPSECRET,
    encrypt_mode = 'normal'
)

wechat = WechatBasic(conf = conf)

class PostResponse():
    def __init__(self, request):
        try:
            wechat.parse_data(data = request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')
        self.id = wechat.message.id
        self.target = wechat.message.target
        self.source = wechat.message.source
        self.time = wechat.message.time
        self.type = wechat.message.type
        self.raw = wechat.message.raw
        self.message = wechat.message
    
    #关注
    def _subscribe(self):
        # 修改DiningTable表中status/seats值
        curr_time = timezone.now()
        index_table = re.findall(r'\d+',self.message.key)[0]
        table = DiningTable.objects.get(index_table=index_table)
        table.status = True
        table.seats += 1
        table.save()
        # 查询Consumer，如果有记录则修改subscribe；如果没有记录，则先从微信获取用户信息，然后新建一条记录
        try:
            consumer = Consumer.objects.get(open_id=self.source)
            if consumer.subscribe == False:
                consumer.subscribe = True
                consumer.on_table = table
        except ObjectDoesNotExist:
            # 通过网页授权获取用户信息
            consumer = Consumer.objects.create(open_id=self.source, on_table=table)
            consumer.create_time = curr_time
        consumer.save()
        # 在Dining表中创建一条记录
        dining = Dining.objects.create(id_table=index_table, consumer=consumer)
        dining.save()
        # 返回选座信息    
        return wechat.response_text(content =  u'您已入座%s号桌' %(index_table))
        
    
    #取消关注
    def _unsubscribe(self):
        # 查找Consumer，将subscribe置为False
        consumer = Consumer.objects.get(open_id=self.source)
        consumer.subscribe = False
        consumer.save()
        return ''
    
    #扫码
    def _scan(self):
        # 修改DiningTable表中status/seats值
        curr_time = timezone.now()
        index_table = self.message.key
        table = DiningTable.objects.get(index_table=index_table)       
        # 查询Consumer, 修改is_dining值为True
        consumer = Consumer.objects.get(open_id=self.source)
        if consumer.on_table.index_table != index_table:
            return wechat.response_text(content =  u'请您先结算%s号桌所抢红包，再扫描该桌'%(consumer.on_table.index_table))
        consumer.on_table = table
        consumer.save()
        table.status = True
        table.seats += 1
        table.save()         
        # 在Dining表中创建一条记录
        dining = Dining.objects.create(id_table=index_table, consumer=consumer)
        dining.save()       
        # 返回选座信息
        return wechat.response_text(content =  u'您已入座%s号桌' %(index_table))
        
        
    #菜单跳转事件
    def _view_jump(self):
        '''结算菜单跳转事件
        1、根据openid,查询consumer，获取当前用户的ownBonusValue,ownTicketValue，idTable.
        2、根据idtable，查询RcvBonus，获取该桌抢到的所有红包
        '''
        return ''
        
    #自动处理
    def auto_handle(self):
        response = wechat.response_text(content='')
        if isinstance(self.message, messages.TextMessage):
            response = wechat.response_text(content=self.message.content)
        elif isinstance(self.message, messages.EventMessage):
            if self.type == 'subscribe':
                response = self._subscribe()
            elif self.type == 'unsubscribe':
                response = self._unsubscribe()
            elif self.type == 'scan':
                response = self._scan()
            elif self.type == 'view':
                pass
        
        return HttpResponse(response, content_type='application/xml')
            
        
