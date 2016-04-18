# -*- coding: utf-8 -*-
'''
import sys

reload(sys)
sys.setdefaultencoding('utf8')
'''

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
            "scene_id": 2
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
                    'url': 'http://120.76.122.53/weixin/snd_bonus'
                },
                {
                    'type': 'view',
                    'name': '抢红包',
                    'url': 'http://120.76.122.53/weixin/rcv_bonus'
                }
            ]
        },        
        {
            'type': 'click',
            'name': '结算',
            'key': 'V1001_TODAY_MUSIC'
        },
        {
            'name': '更多',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '我的钱包',
                    'url': 'http://www.soso.com/'
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

	    

def get_user_info(access_token):
	url = USER_INFO_URL.replace('ACCESS_TOKEN', access_token)
	response = urllib2.urlopen(url)
	user_info = response.read()
	print(user_info)
	return user_info

if __name__ == '__main__':
    #create_qrcode(qrcode, 'table2.jpg')
    #create_menu(menu)
    #user_info = get_user_info(wechat.access_token)
	
	url = USER_INFO_URL.replace('ACCESS_TOKEN', wechat.access_token)
	user_info = UserInfo(url)
	print(user_info.get_name())
	print(user_info.get_sex())
	print(user_info.get_headimgurl())
    
