from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from solo.models import SingletonModel
from finance.models import BalanceUSD, BalanceETG, BalanceETGGOLD, TransactionHistory
import random

class SystemSettings(models.Model):
    is_enable_only_referal_login = models.BooleanField(default=True)
    open_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Финансовые настройки'

    class Meta:
        verbose_name = 'Финансовые настройки'
