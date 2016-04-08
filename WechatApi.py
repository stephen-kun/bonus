# -*- coding: utf-8 -*-
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk import messages

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

if __name__ == '__main__':
    #create_qrcode(qrcode, 'table2.jpg')
    create_menu(menu)
    
