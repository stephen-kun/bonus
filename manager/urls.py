from django.conf.urls import url

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.account, name='account'),

    url(r'^login/$', auth_views.login, {'template_name':'manager/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^bonus_info/$', views.bonus_info, name='bonus_info'),
    url(r'^bonus_info/send_bonus/$', views.send_bonus_list, name="send_bonus_list"),
    url(r'^bonus_info/recv_bonus/$', views.recv_bonus_list, name="recv_bonus_list"),
    url(r'^bonus_info/flying_bonus/$', views.flying_bonus_list, name="flying_bonus_list"),
    url(r'^bonus/create_bonus/$', views.create_bonus, name='create_bonus'),
    url(r'^bonus/sys_bonus_list/$', views.sys_bonus_list, name='sys_bonus_list'),
    url(r'^bonus/create_bonus_action/$', views.create_bonus_action, name='create_bonus_action'),
    url(r'^bonus/bonus_detail/$', views.bonus_detail, name='bonus_detail'),
    url(r'^bonus/bonus_rank_list/$', views.bonus_rank_list, name='bonus_rank_list'),

    url(r'^dining/$', views.dining, name='dining'),
    url(r'^dining/dining_list/$', views.dining_list, name='dining_list'),

    url(r'^account/$', views.account, name='account'),
    url(r'^account/manage/$', views.account_manage, name='account_manage'),
    url(r'^account/create/$', views.account_create, name='create_account'),
    url(r'^account/action/?$', views.action, name='action'),
    url(r'^account/change_password/$', views.change_password, name='change_password'),


    url(r'^account/set_bonus_limit/$', views.set_bonus_limit, name='set_bonus_limit'),
    url(r'^account/create_coupon/$', views.create_coupon, name='create_coupon'),
    url(r'^account/set_coupon_limit/$', views.set_coupon_limit, name='set_coupon_limit'),

    url(r'^basic/$', views.basic, name='basic'),
    url(r'^basic/tables_info/$', views.tables_info, name='tables_info'),
    url(r'^basic/tables_info/add_and_edit$', views.table_item_edit, name='table_item_edit'),
    url(r'^basic/tables_info/table_action', views.table_action, name='table_action'),

    url(r'^basic/goods_info/$', views.goods_info, name='goods_info'),
    url(r'^basic/goods_info/add_and_edit$', views.good_item_edit, name='good_item_edit'),
    url(r'^basic/goods_info/good_action', views.good_action, name='good_action'),

    url(r'^basic/create_bonus/$', views.create_bonus, name='create_bonus'),
    url(r'^basic/create_coupon/$', views.create_coupon, name='create_coupon'),


    url(r'.*', views.index, name='index'),
]
