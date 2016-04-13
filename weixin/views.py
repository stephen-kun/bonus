# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.conf import settings
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages
import urllib2
import json
from .wechat import PostResponse

TOKEN = 'token'
APPID = 'wxc32d7686c0827f2a'
APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'
REDIRECT_URL = 'http://120.76.122.53/weixin/redirect_bonus_snd'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID,REDIRECT_URL)

conf = WechatConf(
    token = TOKEN,
    appid = APPID,
    appsecret = APPSECRET,
    encrypt_mode = 'normal'
)

wechat = WechatBasic(conf = conf)

# Create your views here.

#test asp
@csrf_exempt
def asp_test(request):
	print('recive asp_test request\n')
	response = HttpResponse()
	response['Access-Control-Allow-Origin'] = '*'
	response.write('request ok')
	return response

#发红包	
@csrf_exempt
def snd_bonus(request):
	print('---**snd_bonus**---\n')
	return HttpResponseRedirect(OAUTH_URL)	
	
@csrf_exempt
def redirect_bonus_snd(request): 
	print('---redirect_bonus_snd---\n')
	code = request.GET.get(u'code')
	url = ACCESS_TOKEN_URL.replace('CODE', code)
	response = urllib2.urlopen(url)
	content = response.read()
	access_token = json.loads(content)	
	openid = access_token['openid']
	print('======openid:%s\n' %(openid))
	temp = get_template('fahongbao.html')
	html = temp.render({'STATIC_URL': settings.STATIC_URL, 'openid':openid},request)
	return HttpResponse(html)		

#抢红包
@csrf_exempt
def rcv_bonus(request):
	temp = get_template('qianghongbao.html')
	html = temp.render({'STATIC_URL': settings.STATIC_URL},request)
	return HttpResponse(html)

#抢到的红包
@csrf_exempt
def geted_bonus(request):
	temp = get_template('qiangdaohongbao.html')
	html = temp.render({'STATIC_URL': settings.STATIC_URL},request)
	return HttpResponse(html)
    
@csrf_exempt
def token(request):
	if request.method == 'GET':
		# 检验合法性
		# 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
		signature = request.GET.get('signature')
		timestamp = request.GET.get('timestamp')
		nonce = request.GET.get('nonce')

		if not wechat.check_signature(
				signature, timestamp, nonce):
			return HttpResponseBadRequest('Verify Failed')

		return HttpResponse(
			request.GET.get('echostr', ''), content_type="text/plain")  
	
	PostResponse(request)

