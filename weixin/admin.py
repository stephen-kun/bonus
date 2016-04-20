from django.contrib import admin
from django.conf import settings

from .models import BonusCountDay,BonusCountMonth,DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import Dining,Ticket, RcvBonus, BonusMessage,SndBonus,Recharge, RecordRcvBonus

admin.site.register(BonusCountDay)
admin.site.register(BonusCountMonth)
admin.site.register(DiningTable)
admin.site.register(Consumer)
admin.site.register(Recharge)
admin.site.register(Dining)
admin.site.register(Ticket)
admin.site.register(RcvBonus)
admin.site.register(BonusMessage)
admin.site.register(VirtualMoney)
admin.site.register(SndBonus)
admin.site.register(WalletMoney)
admin.site.register(RecordRcvBonus)



