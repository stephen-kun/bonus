from django.conf.urls import url

#from . import views_design as views
from . import views

urlpatterns = [
	url(r'^view_wechat_token',views.view_wechat_token, name='view_wechat_token'),
	url(r'^view_snd_bonus',views.view_snd_bonus, name='view_snd_bonus'),
	url(r'^view_rcv_bonus',views.view_rcv_bonus, name='view_rcv_bonus'),
	url(r'^view_settle_account',views.view_settle_account, name='view_settle_account'),
	url(r'^view_user_account',views.view_user_account, name='view_user_account'),	
	url(r'^view_redirect_bonus_rcv',views.view_redirect_bonus_rcv, name='view_redirect_bonus_rcv'),
	url(r'^view_geted_bonus',views.view_geted_bonus, name='view_geted_bonus'),
	url(r'^view_ajax_request',views.view_ajax_request, name='view_ajax_request'),
	url(r'^view_redirect_bonus_snd',views.view_redirect_bonus_snd, name='view_redirect_bonus_snd'),
	url(r'^view_common_bonus',views.view_common_bonus, name='view_common_bonus'),
	url(r'^view_random_bonus',views.view_random_bonus, name='view_random_bonus'),	
	url(r'^view_self_rcv_bonus',views.view_self_rcv_bonus, name='view_self_rcv_bonus'),		
	url(r'^view_self_snd_bonus',views.view_self_snd_bonus, name='view_self_snd_bonus'),	
	url(r'^view_self_bonus_list',views.view_self_bonus_list, name='view_self_bonus_list'),		
	url(r'^view_choose_pay',views.view_choose_pay, name='view_choose_pay'),		
	url(r'^view_redirect_settle_account',views.view_redirect_settle_account, name='view_redirect_settle_account'),		
	url(r'^view_redirect_user_account',views.view_redirect_user_account, name='view_redirect_user_account'),		
]
