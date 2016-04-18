from django.contrib import admin
from django.conf import settings

from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,PersonRecharge,SystemRecharge,VirtualMoney
from .models import Dining,Ticket, PersonBonus, SystemBonus, RcvBonus, BonusMessage, SystemMoney, PersonMoney

global null_person_bonus
global null_system_bonus
global null_dining_table
global null_consumer
global null_person_recharge
global null_system_recharge
global null_ticket
global null_rcv_bonus


admin.site.register(BonusCountDay)
admin.site.register(BonusCountMonth)
admin.site.register(DiningTable)
admin.site.register(Consumer)
admin.site.register(PersonRecharge)
admin.site.register(SystemRecharge)
admin.site.register(Dining)
admin.site.register(Ticket)
admin.site.register(PersonBonus)
admin.site.register(SystemBonus)
admin.site.register(RcvBonus)
admin.site.register(BonusMessage)
admin.site.register(SystemMoney)
admin.site.register(PersonMoney)
admin.site.register(VirtualMoney)

null_person_bonus = 1
null_system_bonus = 1
null_dining_table = 1
null_consumer = 1
null_person_recharge = 1
null_system_recharge = 1
null_ticket = 1
null_rcv_bonus = 1

'''
table = DiningTable.objects.all()
table.delete()
table = DiningTable.objects.create(index_table='0')
table.save()


consumer = Consumer.objects.all()
consumer.delete()
consumer = Consumer.objects.create(open_id='2000000000', name='null', on_table=table)
consumer.save()


person_recharge = PersonRecharge.objects.all()
person_recharge.delete()
person_recharge = PersonRecharge.objects.create(id_recharge=2000000000, recharge_person=consumer)
person_recharge.save()

system_recharge = SystemRecharge.objects.all()
system_recharge.delete()
system_recharge = SystemRecharge.objects.create(id_recharge=2000000000)
system_recharge.save()

ticket = Ticket.objects.all()
ticket.delete()
ticket = Ticket.objects.create(id_ticket=2000000000, consumer=consumer)
ticket.save()

person_bonus = PersonBonus.objects.all()
person_bonus.delete()
person_bonus = PersonBonus.objects.create(id_bonus=2000000000, consumer=consumer)
person_bonus.save()

#system_bonus = SystemBonus.objects.all()
#system_bonus.delete()
'''

'''
system_bonus = SystemBonus.objects.all()
system_bonus.delete()
system_bonus = SystemBonus.objects.create(id_bonus=2000000000)
system_bonus.save()

rcv_bonus = RcvBonus.objects.all()
rcv_bonus.delete()
rcv_bonus = RcvBonus.objects.create(id_bonus=2000000000, person_bonus=person_bonus, system_bonus=system_bonus, consumer=consumer, table=table)
rcv_bonus.save()
'''


'''
null_dining_table = DiningTable.objects.get(index_table='0')
null_consumer = Consumer.objects.get(open_id='2000000000')
null_person_recharge = PersonRecharge.objects.get(id_recharge=2000000000)
null_system_recharge = SystemRecharge.objects.get(id_recharge=2000000000)
null_ticket = Ticket.objects.get(id_ticket=2000000000)
null_person_bonus = PersonBonus.objects.get(id_bonus=2000000000)
null_system_bonus = SystemBonus.objects.get(id_bonus=2000000000)
null_rcv_bonus = RcvBonus.objects.get(id_bonus=2000000000)		
'''

