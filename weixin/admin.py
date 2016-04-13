from django.contrib import admin

from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,PersonRecharge,SystemRecharge,VirtualMoney
from .models import Dining,Ticket, PersonBonus, SystemBonus, RcvBonus, BonusMessage, SystemMoney, PersonMoney

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
