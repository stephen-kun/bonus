# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.conf import settings
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages
import re
 
TOKEN = 'token'
APPID = 'wxc32d7686c0827f2a'
APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'

conf = WechatConf(
    token = TOKEN,
    appid = APPID,
    appsecret = APPSECRET,
    encrypt_mode = 'normal'
)

wechat = WechatBasic(conf = conf)

REDIRECT_URL = 'http://ec2-54-200-11-160.us-west-2.compute.amazonaws.com/weixin/snd_bonus'
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URL&response_type=code&scope=snsapi_base&state=1#wechat_redirect"

# Create your views here.

#test asp
@csrf_exempt
def asp_test(request):
	#name = request.POST.get('name')
	#city = request.POST.get('city')
	print('recive asp_test request\n')
	response = HttpResponse()
        response['Access-Control-Allow-Origin'] = 'http://www.w3school.com.cn'
        response.write('request ok')
        return response

#发红包
@csrf_exempt
def snd_bonus_redirect(request):
	temp = get_template('fahongbao.html')
	html = temp.render({'STATIC_URL': settings.STATIC_URL},request)
	return HttpResponse(html)

def snd_bonus(request):
	return HttpResponseRedirect(OAUTH_URL)
	

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

    try:
        wechat.parse_data(data = request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')
    print(request.body)
    print('\n********\n')
    response = wechat.response_text(content ='')
    if isinstance(wechat.message, messages.EventMessage):
        if wechat.message.type == 'subscribe':
            response = wechat.response_text(content = u'您已入座%s号桌' %(re.findall(r'\d+',wechat.message.key)[0]))
        elif wechat.message.type == 'scan':
            response = wechat.response_text(content =  u'您已入座%s号桌' %(wechat.message.key))
    return HttpResponse(response, content_type='application/xml')
