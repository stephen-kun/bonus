from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from category.models import Category
from weixin.models import *

User = get_user_model()


def init_db():
	#初始化用户组
	Group.objects.create(id=1, name='admin')
	Group.objects.create(id=2, name='manager')
	Group.objects.create(id=3, name='consumer')
	#初始化管理员
	user = User.objects.get(username='admin')
	headimgurl = 'http://wx.tonki.com.cn/static/images/admin.png'
	comsumer = Consumer.objects.filter(user=user).update(open_id='0001', name='admin', picture=headimgurl, is_admin=True)
	user.groups.add(Group.objects.get(id=1))
	user.groups.add(Group.objects.get(id=2))	
	#初始化主题
	Category.objects.create(id=1, showimage='', title='default', slug='default', description='', is_global=1, is_closed=0, is_removed=0, parent_id=None)
	#初始化验证码
	AuthCode.objects.create(id_code='123456')
	AuthCode.objects.create(id_code='666666')
	AuthCode.objects.create(id_code='888888')
	#初始化串串
	VirtualMoney.objects.create()
	#初始化桌台
	DiningTable.objects.create(index_table='1')
	DiningTable.objects.create(index_table='2')
	DiningTable.objects.create(index_table='3')
	DiningTable.objects.create(index_table='4')
	DiningTable.objects.create(index_table='5')	
	
