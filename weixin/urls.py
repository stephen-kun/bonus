from django.conf.urls import url

from . import views_design

urlpatterns = [
	url(r'^view_redirect_bonus_rcv',views_design.view_redirect_bonus_rcv, name='view_redirect_bonus_rcv'),
	url(r'^view_geted_bonus',views_design.view_geted_bonus, name='view_geted_bonus'),
	url(r'^view_again_rcv_bonus',views_design.view_again_rcv_bonus, name='view_again_rcv_bonus'),
	url(r'^view_ajax_request',views_design.view_ajax_request, name='view_ajax_request'),
	url(r'^view_redirect_bonus_snd',views_design.view_redirect_bonus_snd, name='view_redirect_bonus_snd'),
	url(r'^view_common_bonus',views_design.view_common_bonus, name='view_common_bonus'),
	url(r'^view_random_bonus',views_design.view_random_bonus, name='view_random_bonus'),	
	url(r'^view_self_rcv_bonus',views_design.view_self_rcv_bonus, name='view_self_rcv_bonus'),		
	url(r'^view_self_snd_bonus',views_design.view_self_snd_bonus, name='view_self_snd_bonus'),	
	url(r'^view_self_bonus_list',views_design.view_self_bonus_list, name='view_self_bonus_list'),		
	url(r'^view_choose_pay',views_design.view_choose_pay, name='view_choose_pay'),		
	url(r'^view_redirect_settle_account',views_design.view_redirect_settle_account, name='view_redirect_settle_account'),		
	url(r'^view_redirect_user_account',views_design.view_redirect_user_account, name='view_redirect_user_account'),		

]
