# -*- coding: utf-8 -*-
# wechat.py
# Create your wechat here.
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages

from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus

from .utils import create_primary_key

from django.core.exceptions import ObjectDoesNotExist 
import pytz
from django.utils import timezone
import re

import urllib
import urllib2
import urlparse
import json

TOKEN = 'token'
APPID = 'wxc32d7686c0827f2a'
APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URI&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)
USER_INFO_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN"


global wechat

conf = WechatConf(
	token = TOKEN,
	appid = APPID,
	appsecret = APPSECRET,
	encrypt_mode = 'normal'
)

SND_BONUS_URL = 'http://120.76.122.53/weixin/view_snd_bonus'
RCV_BONUS_URL = 'http://120.76.122.53/weixin/view_rcv_bonus'
SETTLE_ACCOUNT_URL = 'http://120.76.122.53/weixin/view_settle_account'
USER_ACCOUNT_URL = 'http://120.76.122.53/weixin/view_user_account'

wechat = WechatBasic(conf = conf)

class UserInfo():
	def __init__(self, url):
		self.url = url
		response = urllib2.urlopen(self.url)
		user_info = response.read().decode('utf-8')
		self.user_info = json.loads(user_info)
		
	def get_name(self):
		return self.user_info['nickname']
		
	def get_sex(self):
		return self.user_info['sex']
		
	def get_headimgurl(self):
		return self.user_info['headimgurl']

#用户关注注册
def user_subscribe(openid):
	consumer = None
	try:
		consumer = Consumer.objects.get(open_id=openid)
		if consumer.subscribe == False:
			consumer.subscribe = True
	except ObjectDoesNotExist:
		# 获取用户信息
		url = USER_INFO_URL.replace('ACCESS_TOKEN', wechat.access_token)
		url = url.replace('OPENID', openid)
		user_info = UserInfo(url)
		name = user_info.get_name()
		sex = user_info.get_sex()
		headimgurl = user_info.get_headimgurl()
		consumer = Consumer(open_id=openid, name=name, sex=sex, picture=headimgurl)	
		consumer.subscribe = True
	consumer.save()
	return consumer
	
#更新或创建就餐会话
def update_or_create_session(table, consumer):
	session = None
	consumer_list = Consumer.objects.filter(on_table=table)
	if len(consumer_list):
		session = consumer_list[0].session
	else:
		#创建会话
		session = DiningSession.objects.create(table=table)
	consumer.on_table = table
	consumer.session = session
	consumer.save()
	session.person_num += 1
	session.save()
	table.status = True
	table.save()
	return session
	
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
		#request.session['openid'] = wechat.message.source
	
	#关注
	def _subscribe(self):
		# 查询Consumer，如果有记录则修改subscribe；如果没有记录，则先从微信获取用户信息，然后新建一条记录
		consumer = user_subscribe(self.source)	
		# 获取桌对象
		index_table = re.findall(r'\d+',self.message.key)[0]
		try:
			table = DiningTable.objects.get(index_table=index_table)	
			#更新或创建就餐会话
			session = update_or_create_session(table, consumer)	
			# 返回选座信息    
			return wechat.response_text(content =  u'您已入座%s号桌' %(index_table))
		except ObjectDoesNotExist:
			return wechat.response_text(content = u'该桌台不存在')
		
	#取消关注
	def _unsubscribe(self):
		# 查找Consumer，将subscribe置为False
		consumer = Consumer.objects.get(open_id=self.source)
		if consumer.session and consumer.session.person_num == 1:
			consumer.on_table.status = False
			consumer.on_table.save()
		else:
			consumer.session.person_num -= 1
			consumer.session.save()
		consumer.subscribe = False
		consumer.on_table = None
		consumer.session = None		
		consumer.save()
		return ''
	
	#扫码
	def _scan(self):
		# 获取桌号
		index_table = self.message.key
		table = DiningTable.objects.get_or_create(index_table=index_table)  		
		#判断是否已就坐
		try:
			consumer = Consumer.objects.get(open_id=self.source)
		except ObjectDoesNotExist:
			consumer = user_subscribe(self.source)	
		if consumer.session and consumer.on_table.index_table != index_table:
			return wechat.response_text(content =  u'请您先结算%s号桌所抢红包，再扫描该桌'%(consumer.on_table.index_table))
		elif consumer.session and consumer.on_table.index_table == index_table:
			return ''
		#更新或创建就餐会话		
		session = update_or_create_session(table[0], consumer)	
		# 返回选座信息
		return wechat.response_text(content =  u'您已入座%s号桌' %(index_table))			

		
		
	#菜单跳转事件
	def _view_jump(self):
		'''结算菜单跳转事件
		1、根据openid,查询consumer，获取当前用户的ownBonusValue,ownTicketValue，idTable.
		2、根据idtable，查询RcvBonus，获取该桌抢到的所有红包
		'''
		if self.message.key == SETTLE_ACCOUNT_URL:
			pass
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
				response = self._view_jump()
		
		return HttpResponse(response, content_type='application/xml')
			
		
