from .smsc_api import *
from .models import *
from random import randint
import random
from phonenumber_field.validators import validate_international_phonenumber
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from datetime import datetime, timedelta
from etgProject.celery import app
from django.conf import settings
import redis
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)

def register_new_phonenumber(number):
    phonenumber = UserPhoneNumber.objects.filter(number=number)
    if phonenumber.exists():
        phonenumber = UserPhoneNumber.objects.get(number=number)
        if phonenumber.allready_used() == True:
            raise Exception
    else:
        phonenumber = UserPhoneNumber.objects.create(number=number)
        return True

def send_sms_registration(number):
    #code = str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))
    code = '000'
    redis_instance.set(number,code.encode('utf8'),300)
    #smsc = SMSC()
    #r = smsc.send_sms(number, "Ваш код для продолжения регистрации: " + str(code) + ". Никому не сообщайте его!", sender="sms")
    return True

def send_sms_login(number):
    #code = str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))
    code = '000'
    redis_instance.set(number,code.encode('utf8'),300)
    #smsc = SMSC()
    #r = smsc.send_sms(number, "Ваш код для входа: " + str(code) + ". Никому не сообщайте его!", sender="sms")
    return True

def validateEmail(email):
    if len(email) > 6:
        try:
            validate_email( email )
            return True
        except ValidationError:
            return False
    return False

def validatePass(password):
    if len(password) > 8:
        try:
            validate_password(password=password)
            return True
        except ValidationError:
            return False
    return False

def checkLoginCode(code, user):
    if user.phone_number != None:
        r_code = redis_instance.get(user.char_number).decode('utf8')
        if r_code == None:
            raise Exception('Неверный код')
        if r_code == code:
            redis_instance.delete(user.char_number)
            return True
        else:
            raise Exception('Неверный код')
    else:
        raise Exception('У пользователя отсутствует номер телефона')

@app.task
def send_email_task(head, text,from_email, to_email):
    send_mail(head, text, from_email, [to_email,], fail_silently=False)

def sendEmailVerification(user, host='127.0.0.1:8000', type=1):
    dd = user.next_email_verify_send
    delta = dd - timezone.now()
    if delta.total_seconds() <= 0:
        try:
            letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            code = ''.join(random.choice(letters) for i in range(15))
            id = str(user.pk)
            user.email_code = str(code)
            user.save()
            url = host + '/' + 'verify/' + code + id
            try:
                head = user.name + ', Добро Пожаловать!'
                text = 'Ваш аккаунт усешно зарегестрирован. Осталось подтвердить почту. Перейдите по этой ссылке чтобы подтвердить вашу почту.\nСсылка: ' + str(url)
                from_email = 'etgtestemail@gmail.com'
                to_email = str(user.email)
                send_email_task(head=head, text=text, from_email=from_email, to_email=to_email)
                try:
                    if type == 1:
                        user.next_email_verify_send = timezone.now()
                    else:
                        user.next_email_verify_send = timezone.now() + timedelta(minutes=10)
                    user.save()
                    return True
                except:
                    raise Exception('Проблемы со временем')
            except:
                raise Exception('Нет связи с сервисом почты')
        except:
            raise Exception('Нет связи с сервисом почты')
    else:
        raise Exception('Прошло мало времени с момента прошлой отправки сообщения')


def sendEmailRecovery(user, host='127.0.0.1:8000'):
    try:
        recovery = None
        if RecoveryCode.objects.filter(user=user, is_active=True).exists():
            recovery = RecoveryCode.objects.filter(user=user, is_active=True).first()
        else:
            recovery = RecoveryCode.objects.create(user=user, is_active=True)
            recovery.save()

        url = host + '/' + 'recovery/' + recovery.code
        try:
            head = 'Восстановление'
            text = 'Вы отправили заявку на восстановление пароля. Перейдите по этой ссылке чтобы сменить пароль.\nСсылка: ' + str(url)
            from_email = 'etgtestemail@gmail.com'
            to_email = str(user.email)
            send_email_task(head=head, text=text, from_email=from_email, to_email=to_email)
        except:
            raise Exception('Нет связи с сервисом почты')
    except:
        raise Exception('Нет связи с сервисом почты1')


def registerNewClient(phonenumber, phonecode, email, name, surname, password, rpassword):
    if UserPhoneNumber.objects.filter(number=phonenumber).exists():
        userphonenumber = UserPhoneNumber.objects.get(number=phonenumber)
        if not userphonenumber.phone_number_user.exists():
            if redis_instance.get(str(userphonenumber.number)).decode('utf8') == str(phonecode):
                if validateEmail(email=email):
                    if not User.objects.filter(email=email).exists():
                        if name != '' and surname != '':
                            if password != '':
                                if validatePass(password=password):
                                    if rpassword != '':
                                        if password == rpassword:
                                            user = User.objects.create(email=email,password=make_password(rpassword), phone_number=userphonenumber, name=name, surname=surname, patronymic='',first_login=True,is_email_verified=True)
                                            user.save()
                                        else:
                                            raise Exception('Пароли не совпадают')
                                    else:
                                        raise Exception('Повторите пароль')
                                else:
                                    raise Exception('Слабый пароль')
                            else:
                                raise Exception('Введите пароль')
                        else:
                            raise Exception('Имя и Фамилия должны быть заполнены')
                    else:
                        raise Exception('Пользователь с таким email уже существует')
                else:
                    raise Exception('Неверный формат Email')
            else:
                raise Exception('Неверный код подтверждения')
        else:
            raise Exception('На этот номер уже зарегестрирован пользователь')
    else:
        raise Exception('Ошибка проверки номера')

def updateUser(user, name, surname, patronymic):
    if user.is_authenticated:
        if name != '' and surname != '':
            user.name = name
            user.surname = surname
            user.patronymic = patronymic
            user.save()
            return True
        else:
            raise Exception('Имя и Фамилия не могут быть пустыми')
    else:
        raise Exception('Ошибка авторизации')

def updatePass(user, last, new, rnew):
    if user.is_authenticated:
        if user.check_password(last):
            if new != '' and rnew != '' and new == rnew:
                user.password = make_password(new)
                user.save()
                return True
            else:
                raise Exception('Пароли не могут быть очень простые и должны совпадать')
        else:
            raise Exception('Неверный старый пароль')
    else:
        raise Exception('Ошибка авторизации')

def recoveryPass(user, new, rnew):
    if user.is_authenticated:
        if new != '' and rnew != '' and new == rnew:
            user.password = make_password(new)
            user.save()
            return True
        else:
            raise Exception('Пароли не могут быть очень простые и должны совпадать')
    else:
        raise Exception('Ошибка авторизации')
