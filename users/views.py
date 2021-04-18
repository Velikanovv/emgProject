from django.shortcuts import render, redirect
from users.models import *
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .services import *
from phonenumber_field.validators import validate_international_phonenumber
from django.contrib.auth.password_validation import validate_password
from users import urls
from staff.models import SystemSettings

def verify_email(request, code):
    if request.method == 'GET':
        if len(code) > 15:
            slug = ''
            userid = ''
            for i in range(len(code)):
                if i < 15:
                    slug += code[i]
                else:
                    userid += code[i]
            if User.objects.filter(pk=userid).exists():
                user = User.objects.get(pk=userid)
                if user.email_code == slug:
                    user.email_code = ''
                    user.is_email_verified = True
                    user.save()
                    return render(request, 'client_panel/success_verify_email.html',{})
                else:
                    return render(request, 'client_panel/error_verify_email.html',{})
            else:
                return render(request, 'client_panel/error_verify_email.html',{})
        else:
            return render(request, 'client_panel/error_verify_email.html',{})

def settings_general(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'client_panel/settings.html',{})
        elif request.method == 'POST':
            if request.POST["action"] == 'edit-name':
                name = request.POST["name"]
                surname = request.POST["surname"]
                patronymic = request.POST["patronymic"]
                try:
                    updateUser(user, name=name, surname=surname, patronymic=patronymic)
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST["action"] == 'edit-pass':
                lastpass = request.POST["lastpass"]
                newpass = request.POST["newpass"]
                rnewpass = request.POST["rnewpass"]
                try:
                    updatePass(user,last=lastpass, new=newpass, rnew=rnewpass)
                    login(request=request,user=user)
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST["action"] == 'verify-email':
                host = str(request.get_host())
                try:
                    sendEmailVerification(user, host=host, type=2)
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)


def settings_partners(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'client_panel/settings_partners.html',{})
        elif request.method == 'POST':
            if request.POST["action"] == 'edit-slug':
                slug = request.POST["slug"]
                try:
                    if not user.role == 2:
                        raise Exception('У вас нет прав на изменение реферальной ссылки')
                    if len(slug) < 2:
                        raise Exception('Слишком короткий код')
                    card = ReferalCard.objects.get(user=user)
                    if not ReferalCard.objects.filter(referal_code=slug).exists():
                        card.referal_code = slug
                        card.save()
                        return JsonResponse({}, status=200)
                    else:
                        raise Exception('Такой код уже существует')
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST["action"] == 'verify-email':
                host = str(request.get_host())
                try:
                    sendEmailVerification(user, host=host)
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)

def signin(request):
    user = request.user
    if user.is_authenticated:
        return redirect('client_main')
    if not user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'client_panel/signin.html',{})
        elif request.method == 'POST':
            if request.POST['action'] == 'step-1':
                email = request.POST["email"]
                password = request.POST["password"]
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    request.session['userid'] = str(user.pk)
                    request.session['email'] = email
                    request.session['password'] = password
                    try:
                        send_sms_login(str(user.phone_number.number))
                        return JsonResponse({}, status=200)
                    except:
                        return JsonResponse({'errors': 'Ошибка служб СМС'}, status=400)
                else:
                    return JsonResponse({'errors': 'Неверные данные'}, status=400)
            elif request.POST['action'] == 'step-2':
                email = request.session['email']
                password = request.session['password']
                phonecode = request.POST['phonecode']
                user = User.objects.get(pk=request.session['userid'])
                try:
                    checkLoginCode(phonecode, user)
                    login(request,user=user)
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)



def signup(request):
    user = request.user
    if user.is_authenticated:
        return redirect('client_main')
    s_settings, created = SystemSettings.objects.get_or_create(pk=1)
    if SystemSettings.is_enable_only_referal_login:
        if not 'ref_code' in request.session:
            return render(request, 'client_panel/signup_stop.html',{})
    if not user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'client_panel/signup.html',{})
        elif request.method == 'POST':
            if request.POST['action'] == 'step-1':
                phonenumber = request.POST['phone']
                pn = PhoneNumberField()
                try:
                    validate_international_phonenumber(phonenumber)
                    try:
                        register_new_phonenumber(phonenumber)
                        try:
                            send_sms_registration(phonenumber)
                            return JsonResponse({}, status=200)
                        except:
                            return JsonResponse({'errors': 'СМС Сервис не отвечает, обратитесь в поддержку или попробйте позже'}, status=400)
                    except:
                        return JsonResponse({'errors': 'На этот номер уже зарегестрирован пользователь'}, status=400)
                except:
                    return JsonResponse({'errors': 'Телефон не соответсвует формату'}, status=400)
            elif request.POST['action'] == 'step-2':
                phonenumber = request.POST['phone']
                phonecode = request.POST['phonecode']
                email = request.POST['email']
                name = request.POST['name']
                surname = request.POST['surname']
                password = request.POST['pass']
                rpassword = request.POST['rpass']
                try:
                    print('R1')
                    registerNewClient(phonenumber=phonenumber, phonecode=phonecode, email=email, name=name, surname=surname, password=password, rpassword=rpassword)
                    print('R1')
                    user = authenticate(request, email=email, password=password)
                    host = str(request.get_host())
                    sendEmailVerification(user, host=host, type=1)
                    if user is not None:
                        is_ref = False
                        ref_code = ''
                        if 'ref_code' in request.session:
                            ref_code = request.session['ref_code']
                            is_ref = True
                        if ref_code != '':
                            if ReferalCard.objects.filter(referal_code=ref_code).exists():
                                card = ReferalCard.objects.get(referal_code=ref_code)
                                card.referals_level_1.add(user)
                                card.referal_list.add(user)
                                ReferalsAdded.objects.create(text='1', referal_card=card, level_number='1', user=user).save()
                                card.save()
                                try:
                                    card2 = ReferalCard.objects.get(referals_level_1=card.user)
                                    print(card.user)
                                    if card2 != None:
                                        card2.referals_level_2.add(user)
                                        card2.referal_list.add(user)
                                        ReferalsAdded.objects.create(text='2', referal_card=card2, level_number='2', user=user).save()
                                        card2.save()
                                        try:
                                            card3 = ReferalCard.objects.get(referals_level_1=card2.user)
                                            print(card2.user)
                                            if card3 != None:
                                                card3.referals_level_3.add(user)
                                                card3.referal_list.add(user)
                                                ReferalsAdded.objects.create(text='3', referal_card=card3, level_number='3', user=user).save()
                                                card3.save()
                                                try:
                                                    card4 = ReferalCard.objects.get(referals_level_1=card3.user)
                                                    print(card3.user)
                                                    if card4 != None:
                                                        card4.referals_level_4.add(user)
                                                        card4.referal_list.add(user)
                                                        ReferalsAdded.objects.create(text='4', referal_card=card4, level_number='4', user=user).save()
                                                        card4.save()
                                                        try:
                                                            card5 = ReferalCard.objects.get(referals_level_1=card4.user)
                                                            if card5 != None:
                                                                card5.referals_level_5.add(user)
                                                                card5.referal_list.add(user)
                                                                ReferalsAdded.objects.create(text='5', referal_card=card5, level_number='5', user=user).save()
                                                                card5.save()
                                                                try:
                                                                    card6 = ReferalCard.objects.get(referals_level_1=card5.user)
                                                                    if card6 != None:
                                                                        card6.referals_level_6.add(user)
                                                                        card6.referal_list.add(user)
                                                                        ReferalsAdded.objects.create(text='6', referal_card=card6, level_number='6', user=user).save()
                                                                        card6.save()
                                                                        try:
                                                                            card7 = ReferalCard.objects.get(referals_level_1=card6.user)
                                                                            if card7 != None:
                                                                                card7.referals_level_7.add(user)
                                                                                card7.referal_list.add(user)
                                                                                ReferalsAdded.objects.create(text='7', referal_card=card7, level_number='7', user=user).save()
                                                                                card7.save()
                                                                                try:
                                                                                    card8 = ReferalCard.objects.get(referals_level_1=card7.user)
                                                                                    if card8 != None:
                                                                                        card8.referals_level_8.add(user)
                                                                                        card8.referal_list.add(user)
                                                                                        ReferalsAdded.objects.create(text='8', referal_card=card8, level_number='8', user=user).save()
                                                                                        card8.save()
                                                                                        try:
                                                                                            card9 = ReferalCard.objects.get(referals_level_1=card8.user)
                                                                                            if card9 != None:
                                                                                                card9.referals_level_9.add(user)
                                                                                                card9.referal_list.add(user)
                                                                                                ReferalsAdded.objects.create(text='9', referal_card=card9, level_number='9', user=user).save()
                                                                                                card9.save()
                                                                                                try:
                                                                                                    card10 = ReferalCard.objects.get(referals_level_1=card9.user)
                                                                                                    if card10 != None:
                                                                                                        card10.referals_level_10.add(user)
                                                                                                        card10.referal_list.add(user)
                                                                                                        ReferalsAdded.objects.create(text='10', referal_card=card10, level_number='10', user=user).save()
                                                                                                        card10.save()
                                                                                                except:
                                                                                                    a = 1
                                                                                        except:
                                                                                            a = 1
                                                                                except:
                                                                                    a = 1
                                                                        except:
                                                                            a = 1
                                                                except:
                                                                    a = 1
                                                        except:
                                                            a = 1
                                                except:
                                                    a = 1
                                        except:
                                            a = 1
                                except:
                                    a = 1
                        login(request, user)
                        return JsonResponse({}, status=200)
                    else:
                        return JsonResponse({'errors': 'Неверные данные'}, status=400)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)


def signout(request):
    logout(request)
    return redirect('landing_main')

def pass_recovery(request):
    if request.user.is_authenticated:
        return redirect('client_main')
    if request.method == 'GET':
        return render(request, 'client_panel/pass_recovery.html',{})
    elif request.method == 'POST':
        if request.POST['action'] == 'step-1':
            email = request.POST["email"]
            if User.objects.filter(email=email).exists():
                try:
                    user = User.objects.get(email=email)
                    sendEmailRecovery(user=user, host=request.get_host())
                    return JsonResponse({}, status=200)
                except:
                    return JsonResponse({'errors': 'Ошибка отправки Инструкции'}, status=400)
            else:
                return JsonResponse({'errors': 'Такого пользователя не существует'}, status=400)

def recovery(request, code):
    if request.user.is_authenticated:
        return redirect('client_main')
    if request.method == 'GET':
        return render(request, 'client_panel/recovery.html',{ 'code': code })
    elif request.method == 'POST':
        if request.POST['action'] == 'step-1':
            password = request.POST["pass"]
            rpassword = request.POST["rpass"]
            rec_code = RecoveryCode.objects.get(code=code)
            user = rec_code.user
            if user is not None:
                try:
                    recoveryPass(user=user, new=password, rnew=rpassword)
                    rec_code.is_active = False
                    rec_code.save()
                    return JsonResponse({}, status=200)
                except:
                    return JsonResponse({'errors': 'Ошибка смены пароля'}, status=400)
            else:
                return JsonResponse({'errors': 'Неверные данные'}, status=400)

def settings_redirect(request):
    return redirect('client_settings')

