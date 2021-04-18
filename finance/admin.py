from django.contrib import admin

# Register your models here.
from .models import BalanceETG, BalanceUSD, BalanceETGGOLD, StakingETGHistory, StakingETGGOLDHistory, FinanceSettings, TransactionHistory

from solo.admin import SingletonModelAdmin


admin.site.register(FinanceSettings)

admin.site.register(BalanceETG)
admin.site.register(BalanceETGGOLD)
admin.site.register(BalanceUSD)
admin.site.register(StakingETGHistory)
admin.site.register(StakingETGGOLDHistory)
admin.site.register(TransactionHistory)