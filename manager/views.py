# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http.response import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required

from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from django.contrib.auth import authenticate

@login_required(login_url='/manager/login/')
def index(request):
    current_user = request.user
    return render_to_response("manager/account/account.html")

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/manager/index/")

# 红包统计信息

@login_required(login_url='/manager/login/')
def bonus_info(request):
    return render_to_response("manager/bonus/bonus_info.html")

def send_bonus_statistic(request):
    return render_to_response("manager/bonus/send_bonus_statistic.html")

def recv_bonus_statistic(request):
    return render_to_response("manager/bonus/send_bonus_statistic.html")


# 管理者信息
@login_required(login_url='/manager/login/')
def account(request):
    current_user = request.user
    if(current_user.username == "admin"):
        is_admin = True
    else:
        is_admin = False

    return render_to_response("manager/account/account.html",{'current_user':current_user, 'is_admin':is_admin})

def account_manage(request):
    user_list = User.objects.exclude(username="admin")
    return render_to_response("manager/account/manage_account.html", {'user_list': user_list})

def account_create(request):
    current_user = request.user
    return render_to_response("manager/account/create_account.html")


def _response_json(state, message):
    data = {}
    data['state'] = state
    data['message'] =  message
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def action(request):
    action = request.POST.get("action")
    if(action=="register"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            User.objects.get(username=username)
            return _response_json(1, u"用户名已存在!")
        except ObjectDoesNotExist:
            user=User.objects.create_user(username=username, password=password)
            user.is_staff = True
            user.save()
            return _response_json(0, u"新增用户%s"%(username))
    elif(action=="delete"):
        username = request.POST.get("username")
        try:
            user=User.objects.get(username=username)
            user.is_active = False
            return _response_json(0, u"删除成功!")
        except ObjectDoesNotExist:
            return _response_json(0, u"删除成功!")
    elif(action=="modify_password"):
        username = request.POST.get("username")
        if(request.user.username != "admin"):
            username = request.user.username
            password = request.POST.get("password")
            if password is None:
                return _response_json(1, u"密码不正确!")
            user = authenticate(username=username, password=password)
            if user is None:
                return _response_json(1, u"密码不正确!")

        new_password = request.POST.get("new_password")
        u = User.objects.get(username=username)
        u.set_password(new_password)
        u.save()
        return _response_json(0, u"修改密码成功!")
    else:
        return _response_json(1, u"错误操作")

def change_password(request):
    current_user = request.user
    return render_to_response("manager/account/change_password.html")



def set_coupon_limit(reqeust):
    current_user = request.user
    return render_to_response("manager/account/set_coupon_limit.html")

def create_bonus(request):
    current_user = request.user
    return render_to_response("manager/account/create_bonus.html")

def set_bonus_limit(reqeust):
    current_user = request.user
    return render_to_response("manager/account/set_bonus_limit.html")


#就餐信息
@login_required(login_url='/manager/login/')
def dining(request):
    current_user = request.user
    return render_to_response("manager/dining/dining.html", {'current_user':current_user})

def dining_list(request):
    current_user = request.user
    return render_to_response("manager/dining/dining_list.html")

#店内基本信息
def basic(request):
    return render_to_response("manager/basic/index.html")

def delete_account(request):
    current_user = request.user
    return render_to_response("manager/basic/delete.html")

def create_coupon(request):
    current_user = request.user
    return render_to_response("manager/basic/create_coupon.html")

def goods_info(reqeust):
    return render_to_response("manager/basic/goods_info.html")

def good_item_edit(request):
    return render_to_response("manager/basic/add_edit_good.html")

def tables_info(request):
    return render_to_response("manager/basic/tables_info.html")

def table_item_edit(request):
    return render_to_response("manager/basic/add_edit_table.html")
