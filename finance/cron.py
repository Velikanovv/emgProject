from users.models import *
from finance.models import *

def staking_scheduled_job():
    all_users = User.objects.filter().all()
    for user in all_users:
        if user.balance_etg.balance > 0:
            balance_before = user.balance_etggold.balance
            percent = (user.balance_etg.balance / 100)
            user.balance_etggold.balance += + percent
            user.balance_etggold.staking_full_amount += percent
            user.balance_etggold.save()
            balance_new = user.balance_etggold.balance
            StakingETGGOLDHistory.objects.create(balance=user.balance_etggold,balance_before=balance_before, balance_new=balance_new, staking_amount=percent).save()