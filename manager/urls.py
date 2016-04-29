from django.conf.urls import url

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login/$', auth_views.login, {'template_name':'manager/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^bonus_info/$', views.bonus_info, name='bonus_info'),
    url(r'^bonus_info/send_bonus/$', views.send_bonus_statistic, name="send_bonus_statistic"),
    url(r'^bonus_info/recv_bonus/$', views.send_bonus_statistic, name="send_bonus_statistic"),

    url(r'^dining/$', views.dining, name='dining'),
    url(r'^dining/dining_list/$', views.dining_list, name='dining_list'),

    url(r'^account/$', views.account, name='account'),
    url(r'^account/manage/$', views.account_manage, name='account_manage'),
    url(r'^account/create/$', views.account_create, name='create_account'),
    url(r'^account/action/?$', views.action, name='action'),
    url(r'^account/change_password/$', views.change_password, name='change_password'),
    url(r'^account/create_bonus/$', views.create_bonus, name='create_bonus'),
    url(r'^account/set_bonus_limit/$', views.set_bonus_limit, name='set_bonus_limit'),
    url(r'^account/create_coupon/$', views.create_coupon, name='create_coupon'),
    url(r'^account/set_coupon_limit/$', views.set_coupon_limit, name='set_coupon_limit'),

    url(r'^basic/$', views.basic, name='basic'),
    url(r'^basic/tables_info/$', views.tables_info, name='tables_info'),
    url(r'^basic/tables_info/add_and_edit$', views.table_item_edit, name='table_item_edit'),
    url(r'^basic/goods_info/$', views.goods_info, name='goods_info'),
    url(r'^basic/goods_info/add_and_edit$', views.good_item_edit, name='good_item_edit'),
    url(r'^basic/create_bonus/$', views.create_bonus, name='create_account'),
    url(r'^basic/create_coupon/$', views.create_coupon, name='create_coupon'),


    url(r'.*', views.index, name='index'),
]
