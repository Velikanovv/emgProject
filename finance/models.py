from django.db import models
from django.conf import settings
from django.utils import timezone
from solo.models import SingletonModel
import random

# Create your models here.

class BalanceETG(models.Model):
    balance = models.DecimalField(max_digits=500, decimal_places=9, default=0)
    balance_in_usd = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    staking_full_amount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    staking_full_amount_usd = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    account_code = models.SlugField(unique=True, max_length=10)

    def __str__(self):
        return self.account_code.__str__()

    def save(self, *args, **kwargs):
        if not self.pk:
            letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            code = ''.join(random.choice(letters) for i in range(10))
            while BalanceETG.objects.filter(account_code=code).exists():
                code = ''.join(random.choice(letters) for i in range(10))
            self.account_code = code
            super(BalanceETG, self).save(*args, **kwargs)
        else:
            super(BalanceETG, self).save(*args, **kwargs)
            self.balance_in_usd = self.balance * FinanceSettings.objects.get(pk=1).rateETGinUSD
            self.staking_full_amount_usd = self.staking_full_amount * FinanceSettings.objects.get(pk=1).rateETGinUSD
            super(BalanceETG, self).save()


class BalanceETGGOLD(models.Model):
    balance = models.DecimalField(max_digits=500, decimal_places=9, default=0)
    balance_in_usd = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    staking_full_amount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    staking_full_amount_usd = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    account_code = models.SlugField(unique=True, max_length=10)

    def __str__(self):
        return self.account_code.__str__()

    def save(self, *args, **kwargs):
        if not self.pk:
            letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            code = ''.join(random.choice(letters) for i in range(10))
            while BalanceETGGOLD.objects.filter(account_code=code).exists():
                code = ''.join(random.choice(letters) for i in range(10))
            self.account_code = code
            super(BalanceETGGOLD, self).save(*args, **kwargs)
        else:
            super(BalanceETGGOLD, self).save(*args, **kwargs)
            self.staking_full_amount_usd = self.staking_full_amount * FinanceSettings.objects.get(pk=1).rateETGinUSD
            self.balance_in_usd = self.balance * FinanceSettings.objects.get(pk=1).rateETGinUSD
            super(BalanceETGGOLD, self).save()


class BalanceUSD(models.Model):
    balance = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    account_code = models.SlugField(unique=True, max_length=10)

    def __str__(self):
        return self.account_code.__str__()

    def save(self, *args, **kwargs):
        if not self.pk:
            letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            code = ''.join(random.choice(letters) for i in range(10))
            while BalanceUSD.objects.filter(account_code=code).exists():
                code = ''.join(random.choice(letters) for i in range(10))
            self.account_code = code
            self.balance = 1000000.00
            super(BalanceUSD, self).save(*args, **kwargs)
        else:
            super(BalanceUSD, self).save(*args, **kwargs)


class StakingETGHistory(models.Model):
    balance = models.ForeignKey(BalanceETG, related_name='staking_etg_history', on_delete=models.CASCADE)
    balance_before = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    balance_new = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    staking_amount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    date = models.DateTimeField(default=timezone.now)

class StakingETGGOLDHistory(models.Model):
    balance = models.ForeignKey(BalanceETGGOLD, related_name='staking_etggold_history', on_delete=models.CASCADE)
    balance_before = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    balance_new = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    staking_amount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    date = models.DateTimeField(default=timezone.now)

class FinanceSettings(models.Model):
    etgCount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    etgBuyCount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    realetgBuyCount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    rateETGinUSD = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    rateETGGOLDinUSD = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    rateETGGOLDinETG = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    is_enable_withdrawal = models.BooleanField(default=False)

    def __str__(self):
        return 'Финансовые настройки'

    class Meta:
        verbose_name = 'Системные настройки'

class TransactionHistory(models.Model):
    date = models.DateTimeField(default=timezone.now)

    IN = 1
    OUT = 2
    BETWEEN = 3
    TYPE_NONE = 4

    TRANSACTION_TYPE = (
        (IN, 'Депозит'),
        (OUT, 'Вывод'),
        (BETWEEN, 'Перевод между счетами'),
        (TYPE_NONE, 'Неизвестно'),
    )

    type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE, default=TYPE_NONE)

    SUCCESS = 1
    ERROR = 2
    PROCESS = 3
    NONE = 4

    TRANSACTION_STATUS = (
        (SUCCESS, 'Выполнен'),
        (ERROR, 'Отменен'),
        (PROCESS, 'В процессе'),
        (NONE, 'Неизвестно'),
    )
    status = models.PositiveSmallIntegerField(choices=TRANSACTION_STATUS, default=NONE)

    ETG = 1
    USD = 2
    ETGGOLD = 3
    OUT = 4

    WALLET_TYPE = (
        (ETG, 'ETG'),
        (USD, 'USD'),
        (ETGGOLD, 'ETGGOLD'),
        (OUT, 'ВНЕШНИЙ'),
    )
    from_type = models.PositiveSmallIntegerField(choices=WALLET_TYPE, default=4)

    from_amount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    from_old_balance = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    from_new_balance = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    from_new_balance_in_usd = models.DecimalField(max_digits=500, decimal_places=2, default=0)

    to_type = models.PositiveSmallIntegerField(choices=WALLET_TYPE, default=4)

    to_amount = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    to_amount_in_usd = models.DecimalField(max_digits=500, decimal_places=2, default=0)
    to_old_balance = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    to_new_balance = models.DecimalField(max_digits=500, decimal_places=10, default=0)
    to_new_balance_in_usd = models.DecimalField(max_digits=500, decimal_places=2, default=0)



