from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from solo.models import SingletonModel
from finance.models import BalanceUSD, BalanceETG, BalanceETGGOLD, TransactionHistory
import random

class UserIP(models.Model):
    name = models.CharField(blank=True, max_length=500)
    address = models.GenericIPAddressField(unique=True)
    created = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)
    is_banned = models.BooleanField(default=False)
    ref_code = models.SlugField(max_length=500)

    def __str__(self):
        return self.address

class UserPhoneNumber(models.Model):
    number = PhoneNumberField()
    code = models.CharField(null=True, blank=True, max_length=10)

    def allready_used(self, *args, **kwargs):
        if User.objects.filter(phone_number=self).exists():
            return True
        else:
            return False

    def __str__(self):
        return str(self.number)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    ip = models.ManyToManyField(UserIP,blank=True, related_name='user')
    name = models.CharField(blank=True, max_length=100)
    surname = models.CharField(blank=True, max_length=100)
    patronymic = models.CharField(blank=True, max_length=100)

    phone_number = models.ForeignKey(UserPhoneNumber, null=True, related_name='phone_number_user', on_delete=models.SET_NULL)
    char_number = models.CharField(blank=True,max_length=90)

    balance_etg = models.ForeignKey(BalanceETG, related_name='etg_user', on_delete=models.CASCADE)
    balance_etggold = models.ForeignKey(BalanceETGGOLD, related_name='etggold_user', on_delete=models.CASCADE)
    balance_usd = models.ForeignKey(BalanceUSD, related_name='usd_user', on_delete=models.CASCADE)

    transaction_history = models.ManyToManyField(TransactionHistory,blank=True, related_name="transaction_history_user")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    first_login = models.BooleanField(default=True)
    next_email_verify_send = models.DateTimeField(default=timezone.now)
    email_code = models.CharField(blank=True, max_length=15)
    is_email_verified = models.BooleanField(default=False)

    STANDART = 1
    BLOGGER = 2

    USER_ROLE_CHOICES = (
        (STANDART, 'Стандарт'),
        (BLOGGER, 'Блогер'),
    )
    role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, default=1)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    readonly_fields = [
        'date_joined',
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            balance_usd = BalanceUSD.objects.create(balance=1000000)
            balance_etg = BalanceETG.objects.create()
            balance_etggold = BalanceETGGOLD.objects.create()
            self.balance_etg = balance_etg
            self.balance_usd = balance_usd
            self.balance_etggold = balance_etggold
            super(User, self).save(*args, **kwargs)
            if self.phone_number != None:
                self.char_number = str(self.phone_number.number)
            ref_card = ReferalCard.objects.create(user=self)
            ref_card.save()
            super(User, self).save()
        else:
            if self.phone_number != None:
                self.char_number = str(self.phone_number.number)
            super(User, self).save(*args, **kwargs)

class RecoveryCode(models.Model):
    user = models.ForeignKey(User,related_name='recovery_code', on_delete=models.CASCADE)
    code = models.SlugField(unique=True,max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        if not self.pk:
            letters = 'qwerty-uiopasdfghjklz-xcvbnm1234567890-'
            code = ''.join(random.choice(letters) for i in range(50))
            while RecoveryCode.objects.filter(code=code).exists():
                code = ''.join(random.choice(letters) for i in range(50))
            self.code = code
            super(RecoveryCode, self).save(*args, **kwargs)
        else:
            super(RecoveryCode, self).save(*args, **kwargs)

class ReferalCard(models.Model):
    referal_code = models.CharField(unique=True, max_length=50)
    user = models.OneToOneField(User,related_name='referal_card', on_delete=models.CASCADE)

    level1_percent = models.DecimalField(max_digits=15, decimal_places=2, default=5)
    level2_percent = models.DecimalField(max_digits=15, decimal_places=2, default=3)
    level3_percent = models.DecimalField(max_digits=15, decimal_places=2, default=2)
    level4_percent = models.DecimalField(max_digits=15, decimal_places=2, default=1.5)
    level5_percent = models.DecimalField(max_digits=15, decimal_places=2, default=1)
    level6_percent = models.DecimalField(max_digits=15, decimal_places=2, default=0.5)
    level7_percent = models.DecimalField(max_digits=15, decimal_places=2, default=0.5)
    level8_percent = models.DecimalField(max_digits=15, decimal_places=2, default=0.5)
    level9_percent = models.DecimalField(max_digits=15, decimal_places=2, default=0.5)
    level10_percent = models.DecimalField(max_digits=15, decimal_places=2, default=0.5)

    referals_level_1 = models.ManyToManyField(User, blank=True, related_name='referal_owner1_card')
    referals_level_2 = models.ManyToManyField(User, blank=True, related_name='referal_owner2_card')
    referals_level_3 = models.ManyToManyField(User, blank=True, related_name='referal_owner3_card')
    referals_level_4 = models.ManyToManyField(User, blank=True, related_name='referal_owner4_card')
    referals_level_5 = models.ManyToManyField(User, blank=True, related_name='referal_owner5_card')
    referals_level_6 = models.ManyToManyField(User, blank=True, related_name='referal_owner6_card')
    referals_level_7 = models.ManyToManyField(User, blank=True, related_name='referal_owner7_card')
    referals_level_8 = models.ManyToManyField(User, blank=True, related_name='referal_owner8_card')
    referals_level_9 = models.ManyToManyField(User, blank=True, related_name='referal_owner9_card')
    referals_level_10 = models.ManyToManyField(User, blank=True, related_name='referal_owner10_card')
    all_levels_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)


    level1_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level2_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level3_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level4_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level5_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level6_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level7_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level8_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level9_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    level10_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    referal_list = models.ManyToManyField(User, blank=True, related_name='referal_list_card')


    def __str__(self):
        return self.user.__str__()

    def save(self, *args, **kwargs):
        if not self.pk:
            letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            code = ''.join(random.choice(letters) for i in range(5))
            while ReferalCard.objects.filter(referal_code=code).exists():
                code = ''.join(random.choice(letters) for i in range(5))
            self.referal_code = code
            super(ReferalCard, self).save(*args, **kwargs)
        else:
            super(ReferalCard, self).save(*args, **kwargs)


class ReferalsAdded(models.Model):
    text = models.CharField(blank=True, max_length=500)
    user = models.ForeignKey(User,null=True, related_name='referal_added', on_delete=models.CASCADE)
    referal_card = models.ForeignKey(ReferalCard, on_delete=models.CASCADE)
    level_number = models.CharField(blank=True, max_length=5, default='0')
    date = models.DateTimeField(default=timezone.now)

class AnonymousUser:
    id = None
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def __int__(self):
        raise TypeError('Cannot cast AnonymousUser to int. Are you trying to use it in place of User?')

    def save(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False

    def get_username(self):
        return self.username