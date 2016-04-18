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


table = DiningTable.objects.get_or_create(index_table='0')
null_dining_table=table[0]


consumer = Consumer.objects.get_or_create(open_id='2000000000', name='null', on_table=null_dining_table)
null_consumer=consumer[0]



person_recharge = PersonRecharge.objects.get_or_create(id_recharge=2000000000, recharge_person=null_consumer)
null_person_recharge=person_recharge[0]


system_recharge = SystemRecharge.objects.get_or_create(id_recharge=2000000000)
null_system_recharge=system_recharge[0]


ticket = Ticket.objects.get_or_create(id_ticket=2000000000, consumer=null_consumer)
null_ticket=ticket[0]


person_bonus = PersonBonus.objects.get_or_create(id_bonus=2000000000, consumer=null_consumer)
null_person_bonus=person_bonus[0]



system_bonus = SystemBonus.objects.get_or_create(id_bonus=2000000000)
null_system_bonus=system_bonus[0]


rcv_bonus = RcvBonus.objects.get_or_create(id_bonus=2000000000, person_bonus=null_person_bonus, system_bonus=null_system_bonus, consumer=null_consumer, table=null_dining_table)
null_rcv_bonus=rcv_bonus[0]

