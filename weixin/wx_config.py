# -*- coding: utf-8 -*-

STEPHEN_APPID = 'wxc32d7686c0827f2a'
STEPHEN_APPSECRET = '1981cab986e85ea0aa8e6c13fa2ea59d'

KOOVOX_APPID = 'wxd4dd9f440f125088'
KOOVOX_APPSECRET = '8405baf42ccb5b066393bc93b92a1efd'

QUBABA_APPID = 'wx966e11eecf374549'
QUBABA_APPSECRET = 'b60c602d3af0375af596eaf329319e8b'

TOKEN = 'token'
APPID = STEPHEN_APPID
APPSECRET = STEPHEN_APPSECRET

ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=CODE&grant_type=authorization_code'%(APPID,APPSECRET)
OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=REDIRECT_URL&response_type=code&scope=snsapi_base&state=1#wechat_redirect"%(APPID)
WX_USER_INFO_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN"


#ADDRESS_IP = '127.0.0.1:8000'
#ADDRESS_IP = 'wx.tonki.com.cn'
ADDRESS_IP = '120.76.122.53'

REDIRECT_SSB_URL = 'http://%s/weixin/view_redirect_self_snd_bonus'%(ADDRESS_IP)
REDIRECT_SRB_URL = 'http://%s/weixin/view_redirect_self_rcv_bonus'%(ADDRESS_IP)
REDIRECT_SBL_URL = 'http://%s/weixin/view_redirect_self_bonus_list'%(ADDRESS_IP)
REDIRECT_RB_URL = 'http://%s/weixin/view_redirect_random_bonus'%(ADDRESS_IP)
REDIRECT_CB_URL = 'http://%s/weixin/view_redirect_common_bonus'%(ADDRESS_IP)
REDIRECT_SA_URL = 'http://%s/weixin/view_redirect_settle_account'%(ADDRESS_IP)
REDIRECT_QF_URL = 'http://%s/weixin/view_redirect_qubaba_forum'%(ADDRESS_IP)
REDIRECT_UA_URL = 'http://%s/weixin/view_redirect_user_account'%(ADDRESS_IP)
REDIRECT_BS_URL = 'http://%s/weixin/view_redirect_bonus_snd'%(ADDRESS_IP)
REDIRECT_BR_URL = 'http://%s/weixin/view_redirect_bonus_rcv'%(ADDRESS_IP)
REDIRECT_UT_URL = 'http://%s/weixin/view_redirect_user_ticket'%(ADDRESS_IP)
REDIRECT_UI_URL = 'http://%s/weixin/view_redirect_user_info'%(ADDRESS_IP)
REDIRECT_BD_URL = 'http://%s/weixin/view_redirect_bonus_detail'%(ADDRESS_IP)


AJAX_REQUEST_POST_URL = 'http://%s/weixin/view_ajax_request'%(ADDRESS_IP)
GETED_BONUS_URL = 'http://%s/weixin/view_geted_bonus'%(ADDRESS_IP)
GET_BONUS_URL ='http://%s/weixin/view_rcv_bonus'%(ADDRESS_IP)
SND_BONUS_URL ='http://%s/weixin/view_snd_bonus'%(ADDRESS_IP)
QUBABA_FORUM_URL = 'http://%s/weixin/view_qubaba_forum'%(ADDRESS_IP)
CREATE_COMMON_BONUS_URL = 'http://%s/weixin/view_common_bonus'%(ADDRESS_IP)
CREATE_RANDOM_BONUS_URL = 'http://%s/weixin/view_random_bonus'%(ADDRESS_IP)
SELF_RCV_BONUS_URL = 'http://%s/weixin/view_self_rcv_bonus'%(ADDRESS_IP)
SELF_SND_BONUS_URL = 'http://%s/weixin/view_self_snd_bonus'%(ADDRESS_IP)
SELF_BONUS_LIST_URL = 'http://%s/weixin/view_self_bonus_list'%(ADDRESS_IP)
WEIXIN_PAY_URL = 'http://%s/weixin/wxpay/pay'%(ADDRESS_IP)
USER_ACCOUNT_URL = 'http://%s/weixin/view_user_account'%(ADDRESS_IP)
USER_INFO_URL = 'http://%s/weixin/view_user_info'%(ADDRESS_IP)
USER_TICKET_URL = 'http://%s/weixin/view_user_ticket'%(ADDRESS_IP)
SETTLE_ACCOUNTS_URL = 'http://%s/weixin/view_settle_account'%(ADDRESS_IP)
BONUS_DETAIL_URL = 'http://%s/weixin/view_bonus_detail'%(ADDRESS_IP)