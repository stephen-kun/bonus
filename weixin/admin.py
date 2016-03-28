from django.contrib import admin

from .models import Admin_bonus,Good,Bonus_content,Consumer,DiningTable
from .models import ConsumeInfo,ConsumeRecord,Account
from .models import SndBonus, RcvBonus, AccountContent
from .models import SndBonusContent,RcvBonusContent

class Bonus_contentInline(admin.TabularInline):
    model = Bonus_content
    extra = 0

class AdminBonus(admin.ModelAdmin):
    inlines = [Bonus_contentInline]


admin.site.register(Admin_bonus, AdminBonus)
admin.site.register(Good)


class Account_Inline(admin.TabularInline):
    model = Account
    extra = 1

class Consumer_Account(admin.ModelAdmin):
    inlines = [Account_Inline]

admin.site.register(Consumer, Consumer_Account)
#admin.site.register(Account)

admin.site.register(DiningTable)
admin.site.register(ConsumeInfo)
admin.site.register(ConsumeRecord)
admin.site.register(SndBonus)
admin.site.register(RcvBonus)
admin.site.register(AccountContent)
admin.site.register(SndBonusContent)
admin.site.register(RcvBonusContent)
