# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
# Create your views here.

def index(request):
    return render_to_response("manager/index.html")

# 红包统计信息
def bonus_info(request):
    return render_to_response("manager/bonus/bonus_info.html")

def send_bonus_statistic(request):
    return render_to_response("manager/bonus/send_bonus_statistic.html")

def recv_bonus_statistic(request):
    return render_to_response("manager/bonus/send_bonus_statistic.html")


# 管理者信息
def account(request):
    return render_to_response("manager/account/account.html")

def account_manage(request):
    return render_to_response("manager/account/manage_account.html")

def account_create(request):
    return render_to_response("manager/account/create_account.html")

def change_password(request):
    return render_to_response("manager/account/change_password.html")

def delete_account(request):
    return render_to_response("manager/account/delete.html")

def create_coupon(request):
    return render_to_response("manager/account/create_coupon.html")

def set_coupon_limit(reqeust):
    return render_to_response("manager/account/set_coupon_limit.html")

def create_bonus(request):
    return render_to_response("manager/account/create_bonus.html")

def set_bonus_limit(reqeust):
    return render_to_response("manager/account/set_bonus_limit.html")


#就餐信息
def dining(request):
    return render_to_response("manager/dining/dining.html")

def dining_list(request):
    return render_to_response("manager/dining/dining_list.html")

