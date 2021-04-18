from finance.models import FinanceSettings
from staff.models import SystemSettings
from finance.models import *
from users.models import *
from math import ceil, floor

def float_round(num, places = 0, direction = floor):
    return direction(num * (10**places)) / float(10**places)

def load_finance_settings(request):
    user = request.user
    finance_settings, created = FinanceSettings.objects.get_or_create(pk=1)
    system_settings, created = SystemSettings.objects.get_or_create(pk=1)
    finance_settings.save()
    system_settings.save()
    if user.is_authenticated:
        today_30min = timezone.now() + timezone.timedelta(minutes=30)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if UserIP.objects.filter(address=ip).exists():
            c_ip = UserIP.objects.get(address=ip)
            c_ip.last_activity = timezone.now()
            c_ip.save()
            user.ip.add(c_ip)
        else:
            c_ip = UserIP.objects.create(address=ip)
            c_ip.last_activity = timezone.now()
            c_ip.save()
            user.ip.add(c_ip)
        etg_wallet = BalanceETG.objects.get(etg_user=user)
        usd_wallet = BalanceUSD.objects.get(usd_user=user)
        etggold_wallet = BalanceETGGOLD.objects.get(etggold_user=user)
        etg_balance_in_usd = float_round((etg_wallet.balance * finance_settings.rateETGinUSD), 2, ceil)
        etggold_balance_in_usd = float_round((etggold_wallet.balance * finance_settings.rateETGinUSD), 2, ceil)
        return {'finance_settings': finance_settings, 'etg_wallet': etg_wallet, 'usd_wallet': usd_wallet, 'etggold_wallet': etggold_wallet, 'etg_balance_in_usd': etg_balance_in_usd, 'etggold_balance_in_usd': etggold_balance_in_usd}
    else:
        return {'finance_settings': finance_settings }