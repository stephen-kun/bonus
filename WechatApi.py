# -*- coding: utf-8 -*-
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages

import urllib
import urllib2
import urlparse
import json

TOKEN = 'token'
APPID = 'wxc32d7686c0827f2a'
APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'
OPENID = 'oJvvJwmI3WHtHKDV1N5liNsdMFTU'
USER_INFO_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=%s&lang=zh_CN"%(OPENID)


conf = WechatConf(
    token = TOKEN,
    appid = APPID,
    appsecret = APPSECRET,
    encrypt_mode = 'normal'
)

wechat = WechatBasic(conf = conf)

qrcode = {
    "action_name": "QR_LIMIT_SCENE", 
    "action_info": {
        "scene": {
            "scene_id": 3
        }
    }
}


menu = {
    'button':[
        {
            'name': '红包',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '发红包',
                    'url': 'http://120.76.122.53/weixin/view_snd_bonus'
                },
                {
                    'type': 'view',
                    'name': '抢红包',
                    'url': 'http://120.76.122.53/weixin/view_rcv_bonus'
                }
            ]
        },        
        {
            'type': 'view',
            'name': '结算',
            'url': 'http://120.76.122.53/weixin/view_settle_account'
        },
        {
            'name': '更多',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '我',
                    'url': 'http://120.76.122.53/weixin/view_user_account'
                },
                {
                    'type': 'view',
                    'name': '论坛',
                    'url': 'http://v.qq.com/'
                }
            ]
        }
    ]
}



def create_qrcode(qrcode, filename):
    ticket = wechat.create_qrcode(qrcode)['ticket']
    result = wechat.show_qrcode(ticket)
    with open(filename, 'wb') as fd:
        for chunk in result.iter_content(1024):
            fd.write(chunk)
    print('create qrcode suc!\n')


def create_menu(menu):
    wechat.create_menu(menu)
    print('create menu suc!\n')

def get_user_info(access_token):
	url = USER_INFO_URL.replace('ACCESS_TOKEN', access_token)
	response = urllib2.urlopen(url)
	user_info = response.read().decode('utf-8')
	return user_info

if __name__ == '__main__':
    create_qrcode(qrcode, 'table3.jpg')
    create_menu(menu)
    #get_user_info(wechat.access_token)
    
