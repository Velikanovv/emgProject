from .models import *
from random import randint
import random
from phonenumber_field.validators import validate_international_phonenumber
from django.contrib.auth.password_validation import validate_password
import re
from re import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .cron import staking_scheduled_job
from decimal import Decimal

def buyETG_PayByUsd(user, count):
    finance_settings = FinanceSettings.objects.get(pk=1)
    amount = Decimal(count * finance_settings.rateETGinUSD)
    if count <= finance_settings.etgCount:
        if user.balance_usd.balance >= amount:
            if user.is_email_verified:
                user_old_balance_usd = user.balance_usd.balance
                user_old_balance_etg = user.balance_etg.balance
                s_save = False
                try:
                    old_real_ec = finance_settings.realetgBuyCount
                    balance_usd = user.balance_usd
                    balance_usd.balance = balance_usd.balance - amount
                    balance_usd.save()
                    balance_etg = user.balance_etg
                    balance_etg.balance = balance_etg.balance + count
                    balance_etg.save()
                    finance_settings.etgCount = finance_settings.etgCount - count
                    finance_settings.etgBuyCount += count
                    finance_settings.realetgBuyCount += count
                    finance_settings.save()
                    s_save = True
                    th = TransactionHistory.objects.create(type=3, status=1, from_type=2, from_amount=amount, from_old_balance=user_old_balance_usd, from_new_balance=balance_usd.balance, to_type=1, to_amount=count, to_old_balance=user_old_balance_etg, to_new_balance=balance_etg.balance, to_new_balance_in_usd=(balance_etg.balance*finance_settings.rateETGinUSD), to_amount_in_usd=amount)
                    th.save()
                    user.transaction_history.add(th)
                    return True
                except:
                    if s_save == True:
                        finance_settings.etgBuyCount -= count
                        finance_settings.realetgBuyCount -= count
                        finance_settings.save()

                    user.balance_usd.balance = user_old_balance_usd
                    user.balance_etg.balance = user_old_balance_etg
                    user.balance_etg.save()
                    user.balance_usd.save()
                    th = TransactionHistory.objects.create(type=3, status=2, from_type=2, from_amount=amount, from_old_balance=user_old_balance_usd, from_new_balance=user.balance_usd.balance, to_type=1, to_amount=count, to_old_balance=user_old_balance_etg, to_new_balance=user.balance_etg.balance)
                    th.save()
                    user.transaction_history.add(th)
                    raise Exception('Ошибка осуществления транзакции')
            else:
                raise Exception('Чтобы совершать операции необходимо подтвердить электронную почту. Сделать это можно в настройках.')
        else:
            raise Exception('Недостаточно средств')
    else:
        raise Exception('Превышено максимально доустимое значение')