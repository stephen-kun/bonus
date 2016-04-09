# -*- coding: utf-8 -*-
# wechat.py
# Create your wechat here.
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages

TOKEN = 'token'
APPID = 'wxc32d7686c0827f2a'
APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URI&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)

conf = WechatConf(
    token = TOKEN,
    appid = APPID,
    appsecret = APPSECRET,
    encrypt_mode = 'normal'
)

WECHAT = WechatBasic(conf = conf)

class PostResponse():
	wechat = WECHAT
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
	def _subscribe():
		# 查询Consumer，如果有记录则修改subscribe/is_dining值；如果没有记录，则先从微信获取用户信息，然后新建一条记录
		# 修改DiningTable表中status/seats值
		# 在Dining表中创建一条记录
		# 返回选座信息
		pass
	
	#取消关注
	def _unsubscribe():
		# 查找Consumer，将subscribe置为False
		pass
	
	#扫码
	def _scan():
		# 查询Consumer, 修改is_dining值为True
		# 修改DiningTable表中status/seats值
		# 在Dining表中创建一条记录
		# 返回选座信息
		pass
	
	def replay():
		pass
		