# -*- coding: utf-8 -*-
# utils.py
# Create your utils here.


#红包留言
def action_bonus_message(request):
	#从request中解析出openid,rcv_bonus_id,message
	#在BonusMessage表中创建一条记录
	#修改RcvBonus表中is_message==True
	pass
	
#红包婉拒
def action_bonus_refuse(request):
	#从request中解析出openid,rcv_bonus_id
	#根据rcv_bonus_id在表PersonMoney中找到婉拒的id_money。
	#在PersonRecharge表中创建一条记录
	pass

#微信支付
def action_weixin_pay(request):
	#支付成功，在PersonRecharge表中创建一条新纪录
	#在PersonMoney表中创建相应的记录
	#支付失败，在PersonBonus表删除一条openid的最新的记录
	pass
	
#创建消费券事件
def action_create_ticket(request):
	#从request中解析出openid
	#在Ticket表中创建一条新的记录
	#更新SystemMoney表中ticket字段
	#更新PersonMoney表中ticket字段
	pass


#抢红包事件
def action_get_bonus(request):
	#解析request中openId和tableId
	#抢系统红包：查询SystemBonus表中is_exhausted字段为false的记录，根据结果在RcvBonus表中创建记录，更新SystemMoney表中rcv_bonus字段
	#抢普通红包：查询PersonBonus表中to_table==tableId，根据tableId,查找DiningTable表中seats值，将红包平分，在RcvBonus表中创建记录，更新PersonMoney表中rcv_bonus字段
	#抢手气红包：查询PersonBonus表中bonus_type==手气红包&&is_exhausted==False的记录，根据结果在RcvBonus表中创建记录，更新PersonMoney表中rcv_bonus字段
	#返回抢到的红包个数
	pass
	
#发普通红包事件
def action_set_common_bonus(request):
	#在PersonBonus表中创建一条记录
	#查询Consumer表中own_bonus_detail字段，判断是否需要微信支付
	#如果需要微信支付，计算出需要支付的金额，然后调用微信支付
	pass


#发手气红包事件
def action_set_random_bonus(request):
	#在PersonBonus表中创建一条记录
	#查询Consumer表中own_bonus_detail字段，判断是否需要微信支付
	#如果需要微信支付，计算出需要支付的金额，然后调用微信支付	
	pass

#发系统红包事件
def action_set_system_bonus(request):
	#查询settings.AUTH_USER_MODEL表中own_bonus_detail字段，判断是否需有足够的虚拟钱币
	#如果有足够的虚拟钱币，则在SystemBonus表中创建一条记录，否则提示今日系统红包已派完。
	#更新SystemMoney表中bonus字段值
	pass
	
