# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.template import RequestContext
from django.conf import settings
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages
import re
 


conf = WechatConf(
    token = 'token',
    appid = 'wxc32d7686c0827f2a',
    appsecret = '1981cab986e85ea0aa8e6c13fa2ea59d',
    encrypt_mode = 'normal'
)

wechat = WechatBasic(conf = conf)

# Create your views here.

#抢红包
def rcv_bonus(request):
    temp = get_template('qianghongbao.html')
    html = temp.render(RequestContext(request,{'STATIC_URL': settings.STATIC_URL}))
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
