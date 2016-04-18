# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.conf import settings
import urllib2
import json
from .wechat import PostResponse, wechat, TOKEN, APPID, APPSECRET
from .utils import  action_get_bonus


REDIRECT_BS_URL = 'http://120.76.122.53/weixin/redirect_bonus_snd'
REDIRECT_BR_URL = 'http://120.76.122.53/weixin/view_redirect_bonus_rcv'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URL&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)

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
	url = OAUTH_URL.replace('REDIRECT_URL', REDIRECT_BS_URL)
	return HttpResponseRedirect(url)	
	
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
	
#抢红包界面
@csrf_exempt
def view_rcv_bonus(request):
	print('---**view_rcv_bonus**---\n')
	url = OAUTH_URL.replace('REDIRECT_URL', REDIRECT_BR_URL)
	return HttpResponseRedirect(url)	
	
#抢红包界面认证
@csrf_exempt
def view_redirect_bonus_rcv(request):
	#获取openid
	#刷新页面中openid
	print('---view_redirect_bonus_rcv---\n')
	print(request.get_host())
	code = request.GET.get(u'code')
	url = ACCESS_TOKEN_URL.replace('CODE', code)
	response = urllib2.urlopen(url)
	content = response.read()
	access_token = json.loads(content)	
	openid = access_token['openid']
	print('======openid:%s\n' %(openid))
	temp = get_template('qianghongbao.html')
	html = temp.render({'STATIC_URL': settings.STATIC_URL, 'openid':openid},request)	
	return HttpResponse(html)

#抢到的红包
@csrf_exempt
def geted_bonus(request):
	temp = get_template('qiangdaohongbao.html')
	html = temp.render({'STATIC_URL': settings.STATIC_URL},request)
	return HttpResponse(html)
	
#抢红包动作
@csrf_exempt
def view_action_get_bonus(request):
	print('***view_action_get_bonus ***\n')
	print(request.body)
	openid = request.body
	action_get_bonus(openid)
	return HttpResponse('ok')
    
@csrf_exempt
def token(request):
	if request.method == 'GET':
		# 检验合法性
		# 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
		signature = request.GET.get('signature')
		timestamp = request.GET.get('timestamp')
		nonce = request.GET.get('nonce')

		if not wechat.check_signature(signature, timestamp, nonce):
			return HttpResponseBadRequest('Verify Failed')

		return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")  
	
	response = PostResponse(request)
	return response.auto_handle()

