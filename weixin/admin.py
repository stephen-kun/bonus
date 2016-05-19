from django.contrib import admin


from .models import DiningTable,Consumer,VirtualMoney, WalletMoney
from .models import DiningSession,Ticket, RcvBonus,SndBonus,Recharge, RecordRcvBonus

class MoneyInline(admin.TabularInline):
	model = WalletMoney
	extra = 1
	
class RcvBonusInline(admin.TabularInline):
	model = RcvBonus
	extra = 1

class SndBonusInline(admin.TabularInline):
	model = SndBonus
	extra = 1	
	
class RechargeWalletMoney(admin.ModelAdmin):
	inlines = [MoneyInline]

class SndBonusWalletMoney(admin.ModelAdmin):
	inlines = [RcvBonusInline, MoneyInline]
	
class RcvBonusWalletMoney(admin.ModelAdmin):
	inlines = [MoneyInline]
	
class TicketWalletMoney(admin.ModelAdmin):
	inlines = [MoneyInline]
	
class ConumerBonus(admin.ModelAdmin):
	inlines = [RcvBonusInline, SndBonusInline]
	
#admin.site.register(Consumer, ConumerBonus)	
admin.site.register(Recharge, RechargeWalletMoney)
admin.site.register(SndBonus, SndBonusWalletMoney)
admin.site.register(RcvBonus, RcvBonusWalletMoney)
admin.site.register(Ticket, TicketWalletMoney)


admin.site.register(DiningTable)
admin.site.register(Consumer)
#admin.site.register(Recharge)
admin.site.register(DiningSession)
#admin.site.register(Ticket)
#admin.site.register(RcvBonus)
admin.site.register(VirtualMoney)
#admin.site.register(SndBonus)
admin.site.register(WalletMoney)
admin.site.register(RecordRcvBonus)



