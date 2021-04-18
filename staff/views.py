from django.shortcuts import render, redirect
from users.models import *
from landing.models import *
from staff.models import *
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .services import *
from phonenumber_field.validators import validate_international_phonenumber
from django.contrib.auth.password_validation import validate_password
from users import urls
from django.db.models import Q
from finance.services import buyETG_PayByUsd
from decimal import Decimal
from finance.models import *
import datetime as DT


def main(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':

            return render(request, 'staff_panel/main.html',{})

def news_create(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'staff_panel/news_create.html', {})
        elif request.method == 'POST':
            if request.POST['action'] == 'create':
                try:
                    title = request.POST['title']
                    text = request.POST['text']
                    date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y') + DT.timedelta(hours=timezone.now().hour, minutes=timezone.now().minute)
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        new = News.objects.create(title=title, text=text, picture=pic, date=date)
                        new.save()
                    else:
                        new = News.objects.create(title=title, text=text, date=date)
                        new.save()
                    return JsonResponse({}, status=200)
                except:
                    return JsonResponse({'errors': 'Ошибка при создании'}, status=400)

def news_edit(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            if News.objects.filter(pk=pk).exists():
                new = News.objects.get(pk=pk)
                return render(request, 'staff_panel/news_edit.html',{'new': new})
            else:
                return redirect('staff_news')
        elif request.method == 'POST':
            if News.objects.filter(pk=pk).exists():
                if request.POST['action'] == 'save':
                    try:
                        new = News.objects.get(pk=pk)
                        title = request.POST['title']
                        text = request.POST['text']
                        if new.date.date() != DT.datetime.strptime(request.POST['date'], '%m/%d/%Y').date():
                            date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y') + DT.timedelta(hours=timezone.now().hour, minutes=timezone.now().minute)
                        else:
                            date = new.date
                        if 'img' in request.FILES:
                            pic = request.FILES.get('img')
                            new.title = title
                            new.text = text
                            new.picture = pic
                            new.date = date
                            new.save()
                        else:
                            new.title = title
                            new.text = text
                            new.date = date
                            new.save()
                        return JsonResponse({}, status=200)
                    except:
                        return JsonResponse({'errors': 'Ошибка при создании'}, status=400)
            if request.POST['action'] == 'delete':
                try:
                    new = News.objects.get(pk=pk)
                    new.delete()
                    return JsonResponse({}, status=200)
                except:
                    return JsonResponse({'errors': 'Ошибка при удалении'}, status=400)

def news(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            news = News.objects.all().order_by('-date')
            return render(request, 'staff_panel/news.html',{'news': news})

def faq_create(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'staff_panel/faq_create.html', {})
        elif request.method == 'POST':
            if request.POST['action'] == 'create':
                try:
                    title = request.POST['title']
                    text = request.POST['text']
                    faq = Faq.objects.create(title=title, text=text)
                    faq.save()
                    return JsonResponse({}, status=200)
                except:
                    return JsonResponse({'errors': 'Ошибка при создании'}, status=400)

def faq_edit(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            if Faq.objects.filter(pk=pk).exists():
                faq = Faq.objects.get(pk=pk)
                return render(request, 'staff_panel/faq_edit.html',{'faq': faq})
            else:
                return redirect('staff_faqs')
        elif request.method == 'POST':
            if Faq.objects.filter(pk=pk).exists():
                if request.POST['action'] == 'save':
                    try:
                        title = request.POST['title']
                        text = request.POST['text']
                        faq = Faq.objects.get(pk=pk)
                        faq.title = title
                        faq.text = text
                        faq.save()
                        return JsonResponse({}, status=200)
                    except:
                        return JsonResponse({'errors': 'Ошибка при сохранении'}, status=400)
                if request.POST['action'] == 'delete':
                    try:
                        faq = Faq.objects.get(pk=pk)
                        faq.delete()
                        return JsonResponse({}, status=200)
                    except:
                        return JsonResponse({'errors': 'Ошибка при удалении'}, status=400)

def faqs(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            faqs = Faq.objects.all().order_by('-date')
            return render(request, 'staff_panel/faqs.html',{'faqs': faqs})

def roadmap_create(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'staff_panel/roadmap_create.html', {})
        elif request.method == 'POST':
            if request.POST['action'] == 'create':
                try:
                    title = request.POST['title']
                    date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y')
                    map = RoadMap.objects.create(title=title, date=date)
                    map.save()
                    return JsonResponse({}, status=200)
                except:
                    return JsonResponse({'errors': 'Ошибка при создании'}, status=400)

def roadmap_edit(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            if RoadMap.objects.filter(pk=pk).exists():
                map = RoadMap.objects.get(pk=pk)
                return render(request, 'staff_panel/roadmap_edit.html',{'map': map})
            else:
                return redirect('staff_roadmap')
        elif request.method == 'POST':
            if RoadMap.objects.filter(pk=pk).exists():
                if request.POST['action'] == 'save':
                    try:
                        title = request.POST['title']
                        date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y')
                        map = RoadMap.objects.get(pk=pk)
                        map.title = title
                        map.date = date
                        map.save()
                        return JsonResponse({}, status=200)
                    except:
                        return JsonResponse({'errors': 'Ошибка при сохранении'}, status=400)
                if request.POST['action'] == 'delete':
                    try:
                        map = RoadMap.objects.get(pk=pk)
                        map.delete()
                        return JsonResponse({}, status=200)
                    except:
                        return JsonResponse({'errors': 'Ошибка при удалении'}, status=400)

def roadmap(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            maps = RoadMap.objects.all().order_by('-date')
            return render(request, 'staff_panel/roadmap.html',{'maps': maps})

def user_percent(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        usr = User.objects.get(pk=pk)
        if request.method == 'GET':
            if usr.role == 2:
                return render(request, 'staff_panel/percent.html',{ 'c_user': usr })
            else:
                return redirect('staff_user_view', usr.pk)
        if request.method == 'POST':
            if 'savepercent' in request.POST:
                try:
                    usr.referal_card.level1_percent = request.POST['p_level_1']
                    usr.referal_card.level2_percent = request.POST['p_level_2']
                    usr.referal_card.level3_percent = request.POST['p_level_3']
                    usr.referal_card.level4_percent = request.POST['p_level_4']
                    usr.referal_card.level5_percent = request.POST['p_level_5']
                    usr.referal_card.level6_percent = request.POST['p_level_6']
                    usr.referal_card.level7_percent = request.POST['p_level_7']
                    usr.referal_card.level8_percent = request.POST['p_level_8']
                    usr.referal_card.level9_percent = request.POST['p_level_9']
                    usr.referal_card.level10_percent = request.POST['p_level_10']
                    usr.referal_card.save()
                    usr = User.objects.get(pk=pk)
                    if usr.role == 2:
                        return render(request, 'staff_panel/percent.html',{ 'c_user': usr,'success':'1','error':''})
                    else:
                        return redirect('staff_user_view', usr.pk)
                except Exception as e:
                    usr = User.objects.get(pk=pk)
                    if usr.role == 2:
                        return render(request, 'staff_panel/percent.html',{ 'c_user': usr,'success':'2','error':e.args[0]})
                    else:
                        return redirect('staff_user_view', usr.pk)

def system_settings(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'staff_panel/system_settings.html', { 's_settings': SystemSettings.objects.get(pk=1) })
        if request.method == 'POST':
            if 'referal_login' in request.POST:
                setting, created = SystemSettings.objects.get_or_create(pk=1)
                old = setting.is_enable_only_referal_login
                try:
                    if setting.is_enable_only_referal_login:
                        setting.is_enable_only_referal_login = False
                        setting.save()
                        return render(request, 'staff_panel/system_settings.html',{ 's_settings': SystemSettings.objects.get(pk=1),'success': '4','error': ''})
                    else:
                        setting.is_enable_only_referal_login = True
                        setting.save()
                        return render(request, 'staff_panel/system_settings.html',{ 's_settings': SystemSettings.objects.get(pk=1),'success': '3','error': ''})
                except Exception as e:
                    setting.is_enable_only_referal_login = old
                    setting.save()
                    return render(request, 'staff_panel/system_settings.html',{ 's_settings': SystemSettings.objects.get(pk=1),'success': '2','error': e.args[0] })

def finance_settings(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'staff_panel/finance_settings.html',{ 'f_settings': FinanceSettings.objects.get(pk=1) })
        if request.method == 'POST':
            if 'savesettings' in request.POST:
                etginusd = request.POST['etginusd']
                etgcount = request.POST['etg-count']
                setting = FinanceSettings.objects.get(pk=1)
                old_etginusd = setting.rateETGinUSD
                old_etgcount = setting.etgCount
                try:
                    setting.rateETGinUSD = etginusd
                    setting.etgCount = etgcount
                    setting.save()
                    return render(request, 'staff_panel/finance_settings.html',{ 'f_settings': FinanceSettings.objects.get(pk=1),'success': '1','error': ''})
                except Exception as e:
                    setting.rateETGinUSD = old_etginusd
                    setting.etgCount = old_etgcount
                    setting.save()
                    return render(request, 'staff_panel/finance_settings.html',{ 'f_settings': FinanceSettings.objects.get(pk=1),'success': '2','error': e.args[0] })
            if 'withdrawal' in request.POST:
                setting = FinanceSettings.objects.get(pk=1)
                old = setting.is_enable_withdrawal
                try:
                    if setting.is_enable_withdrawal:
                        setting.is_enable_withdrawal = False
                        setting.save()
                        return render(request, 'staff_panel/finance_settings.html',{ 'f_settings': FinanceSettings.objects.get(pk=1),'success': '4','error': ''})
                    else:
                        setting.is_enable_withdrawal = True
                        setting.save()
                        return render(request, 'staff_panel/finance_settings.html',{ 'f_settings': FinanceSettings.objects.get(pk=1),'success': '3','error': ''})
                except Exception as e:
                    setting.is_enable_withdrawal = old
                    setting.save()
                    return render(request, 'staff_panel/finance_settings.html',{ 'f_settings': FinanceSettings.objects.get(pk=1),'success': '2','error': e.args[0] })


def user_view(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        usr = User.objects.get(pk=pk)
        if request.method == 'GET':
            return render(request, 'staff_panel/user.html',{ 'c_user': usr })
        if request.method == 'POST':
            if request.POST['action'] == 'block':
                try:
                    if not usr.is_superuser:
                        usr.is_active = False
                        usr.is_banned = True
                        usr.save()
                        return JsonResponse({}, status=200)
                    else:
                        return JsonResponse({'errors': 'Данного пользователя нельзя блокировать'}, status=400)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST['action'] == 'unblock':
                try:
                    usr.is_active = True
                    usr.is_banned = False
                    usr.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST['action'] == 'giveadmin':
                try:
                    usr.is_staff = True
                    usr.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST['action'] == 'ungiveadmin':
                try:
                    if not usr.is_superuser:
                        usr.is_staff = False
                        usr.save()
                        return JsonResponse({}, status=200)
                    else:
                        return JsonResponse({'errors': 'У данного пользователя нельзя забрать статус администартора'}, status=400)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST['action'] == 'givebloger':
                try:
                    usr.role = 2
                    usr.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)
            if request.POST['action'] == 'ungivebloger':
                try:
                    usr.role = 1
                    usr.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': e.args[0]}, status=400)

def user_transactions(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            usr = User.objects.get(pk=pk)
            history = TransactionHistory.objects.filter(transaction_history_user=usr).order_by('-date').all()
            return render(request, 'staff_panel/transactions.html',{ 'c_user': usr,'history': history })

def user_ips(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            usr = User.objects.get(pk=pk)
            ips = UserIP.objects.filter(user=usr).order_by('-last_activity').all()
            return render(request, 'staff_panel/ips.html',{ 'c_user': usr,'ips': ips })

def user_give_etg(request, pk):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            usr = User.objects.get(pk=pk)
            return render(request, 'staff_panel/give_etg.html',{ 'c_user': usr })
        elif request.method == 'POST':
            if 'action' in request.POST:
                if request.POST['action'] == 'buy-etg':
                    count = request.POST['count']
                    try:
                        c_user = User.objects.get(pk=pk)
                        etg_balance = c_user.balance_etg.balance
                        usd_balance = c_user.balance_usd.balance
                        try:
                            c_user.balance_usd.balance += Decimal(Decimal(count) * FinanceSettings.objects.get(pk=1).rateETGinUSD)
                            c_user.balance_usd.save()
                            buyETG_PayByUsd(user=c_user, count=Decimal(count))
                            c_user.balance_usd.balance = usd_balance
                            c_user.balance_usd.save()
                            return JsonResponse({}, status=200)
                        except Exception as e:
                            c_user.balance_usd.balance = usd_balance
                            c_user.balance_etg.balance = etg_balance
                            c_user.balance_usd.save()
                            return JsonResponse({'errors': e.args[0]}, status=400)
                    except Exception as e:
                        return JsonResponse({'errors': e.args[0]}, status=400)

def users(request):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            sort = request.GET.get("sort","")
            type = request.GET.get("type", "")
            status = request.GET.get("status", "")
            show = 10
            page = 1
            if request.GET.get("show", "").isdigit():
                show = int(request.GET.get("show", ""))
            else:
                show = 10
            if request.GET.get("page", "").isdigit():
                page = int(request.GET.get("page", ""))
            else:
                page = 1
            filter_type = 0
            is_banned = False
            is_active = False
            if status == 'active':
                is_active = True
                is_banned = False
                filter_type = 1
            elif status == 'blocked':
                is_active = False
                is_banned = True
                filter_type = 1
            else:
                filter_type = 0

            type_type = 0
            is_staff = False
            role = 1
            if type == 'staff':
                is_staff = True
                type_type = 1
            elif type == 'blogger':
                is_staff = False
                role = 2
                type_type = 2
            elif type == 'standart':
                is_staff = False
                role = 1
                type_type = 2
            else:
                status_type = 0

            all_users = None
            users_count = User.objects.all().count()

            order = ''
            if sort == 'etgup':
                order = 'balance_etg__balance'
            if sort == 'etgdown':
                order = '-balance_etg__balance'
            if sort == 'usdup':
                order = 'balance_usd__balance'
            if sort == 'usddown':
                order = '-balance_usd__balance'

            if filter_type == 1:
                if type_type == 0:
                    if order == '':
                        all_users = User.objects.filter(is_active=is_active, is_banned=is_banned).all()
                    else:
                        all_users = User.objects.filter(is_active=is_active, is_banned=is_banned).all().order_by(order)
                elif type_type == 1:
                    if order == '':
                        all_users = User.objects.filter(is_active=is_active, is_banned=is_banned, is_staff=is_staff).all()
                    else:
                        all_users = User.objects.filter(is_active=is_active, is_banned=is_banned, is_staff=is_staff).all().order_by(order)
                elif type_type == 2:
                    if order == '':
                        all_users = User.objects.filter(is_active=is_active, is_banned=is_banned, is_staff=is_staff, role=role).all()
                    else:
                        all_users = User.objects.filter(is_active=is_active, is_banned=is_banned, is_staff=is_staff, role=role).all().order_by(order)
                else:
                    if order == '':
                        all_users = User.objects.all()
                    else:
                        all_users = User.objects.all().order_by(order)
            else:
                if type_type == 0:
                    if order == '':
                        all_users = User.objects.all()
                    else:
                        all_users = User.objects.all().order_by(order)
                elif type_type == 1:
                    if order == '':
                        all_users = User.objects.filter(is_staff=is_staff).all()
                    else:
                        all_users = User.objects.filter(is_staff=is_staff).all().order_by(order)
                elif type_type == 2:
                    if order == '':
                        all_users = User.objects.filter(is_staff=is_staff, role=role).all()
                    else:
                        all_users = User.objects.filter(is_staff=is_staff, role=role).all().order_by(order)
                else:
                    if order == '':
                        all_users = User.objects.all()
                    else:
                        all_users = User.objects.all().order_by(order)

            """Пагинация"""
            row_count = show
            current_page = page
            start = 0 + (row_count*(current_page-1));
            end = row_count + (row_count*(current_page-1));
            users = all_users[start:end]
            page_count = float(all_users.count()) / float(row_count)
            if page_count > int(page_count):
                page_count += 1
            page_count = int(page_count)
            prev_page = current_page - 1
            next_page = current_page + 1
            pages = []
            for i in range(1, page_count+1):
                pages.append(i)

            s = 1;
            e = 2;
            if current_page == 1:
                s = 1
                e = 5
            elif current_page == 2 or current_page == 3:
                s = 1
                e = 5
            elif current_page == page_count-2 or current_page == page_count-1:
                s = page_count-4
                e = page_count
            elif current_page == page_count:
                s = page_count-4
                e = page_count
            else:
                s = current_page - 2
                e = current_page + 2
            center_pages = []
            for k in range(s, e+1):
                center_pages.append(k)
            pp = page_count - 2
            cc = page_count - 1
            param_count = 0
            params = ''
            if request.GET.get("type", "") != '':
                params += '?type=' + str(type)
                param_count += 1
            if request.GET.get("status", "") != '':
                if param_count > 0:
                    params += '&status=' + str(status)
                else:
                    params += '?status=' + str(status)
                param_count += 1
            if request.GET.get("show", "") != '':
                if param_count > 0:
                    params += '&show=' + str(show)
                else:
                    params += '?show=' + str(show)
                param_count += 1

            if request.GET.get("sort", "") != '':
                if param_count > 0:
                    params += '&sort=' + str(sort)
                else:
                    params += '?sort=' + str(sort)
                param_count += 1

            if param_count > 0:
                params += '&page='
            else:
                params += '?page='
                param_count += 1
            return render(request, 'staff_panel/users.html',{'users': users, 'users_count': users_count,'page_count': page_count, 'current_page': current_page, 'prev_page':prev_page, 'next_page': next_page, 'pages':pages, 'center_pages': center_pages, 'pp': pp, 'cc':cc,'show':show,'type': type,'status': status,'sort':sort, 'params': params})
        if request.method == 'POST' and 'text' in request.POST:
            search_text = request.POST['text']
            sort = request.GET.get("sort","")
            type = request.GET.get("type", "")
            status = request.GET.get("status", "")
            show = 10
            page = 1
            if request.GET.get("show", "").isdigit():
                show = int(request.GET.get("show", ""))
            else:
                show = 10
            if request.GET.get("page", "").isdigit():
                page = int(request.GET.get("page", ""))
            else:
                page = 1
            filter_type = 0
            is_banned = False
            is_active = False
            if status == 'active':
                is_active = True
                is_banned = False
                filter_type = 1
            elif status == 'blocked':
                is_active = False
                is_banned = True
                filter_type = 1
            else:
                filter_type = 0

            type_type = 0
            is_staff = False
            role = 1
            if type == 'staff':
                is_staff = True
                type_type = 1
            elif type == 'blogger':
                is_staff = False
                role = 2
                type_type = 2
            elif type == 'standart':
                is_staff = False
                role = 1
                type_type = 2
            else:
                status_type = 0

            all_users = None
            users_count = User.objects.all().count()

            order = ''
            if sort == 'etgup':
                order = 'balance_etg__balance'
            if sort == 'etgdown':
                order = '-balance_etg__balance'
            if sort == 'usdup':
                order = 'balance_usd__balance'
            if sort == 'usddown':
                order = '-balance_usd__balance'
            search_text = str(search_text)
            if filter_type == 1:
                if type_type == 0:
                    if order == '':
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_banned=is_banned)) ).all()
                    else:
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_banned=is_banned)) ).all().order_by(order)
                elif type_type == 1:
                    if order == '':
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_banned=is_banned) & Q(is_staff=is_staff))).all()
                    else:
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_banned=is_banned) & Q(is_staff=is_staff))).all().order_by(order)
                elif type_type == 2:
                    if order == '':
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_banned=is_banned) & Q(is_staff=is_staff) & Q(role=role))).all()
                    else:
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text) ) & (Q(is_active=is_active) & Q(is_banned=is_banned) & Q(is_staff=is_staff) & Q(role=role))).all().order_by(order)
                else:
                    if order == '':
                        all_users = User.objects.filter((Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text) ))
                    else:
                        all_users = User.objects.filter((Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text) )).order_by(order)
            else:
                if type_type == 0:
                    if order == '':
                        all_users = User.objects.filter((Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)))
                    else:
                        all_users = User.objects.filter((Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text))).order_by(order)
                elif type_type == 1:
                    if order == '':
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_staff=is_staff)) ).all()
                    else:
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_staff=is_staff)) ).all().order_by(order)
                elif type_type == 2:
                    if order == '':
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_staff=is_staff) & Q(role=role)) ).all()
                    else:
                        all_users = User.objects.filter( (Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)) & (Q(is_active=is_active) & Q(is_staff=is_staff) & Q(role=role)) ).all().order_by(order)
                else:
                    if order == '':
                        all_users = User.objects.filter((Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text)))
                    else:
                        all_users = User.objects.filter((Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(surname__icontains=search_text) | Q(patronymic__icontains=search_text) | Q(char_number__icontains=search_text))).order_by(order)

            """Пагинация"""
            row_count = show
            current_page = page
            start = 0 + (row_count*(current_page-1));
            end = row_count + (row_count*(current_page-1));
            users = all_users[start:end]
            page_count = float(all_users.count()) / float(row_count)
            if page_count > int(page_count):
                page_count += 1
            page_count = int(page_count)
            prev_page = current_page - 1
            next_page = current_page + 1
            pages = []
            for i in range(1, page_count+1):
                pages.append(i)

            s = 1;
            e = 2;
            if current_page == 1:
                s = 1
                e = 5
            elif current_page == 2 or current_page == 3:
                s = 1
                e = 5
            elif current_page == page_count-2 or current_page == page_count-1:
                s = page_count-4
                e = page_count
            elif current_page == page_count:
                s = page_count-4
                e = page_count
            else:
                s = current_page - 2
                e = current_page + 2
            center_pages = []
            for k in range(s, e+1):
                center_pages.append(k)
            pp = page_count - 2
            cc = page_count - 1
            param_count = 0
            params = ''
            if request.GET.get("type", "") != '':
                params += '?type=' + str(type)
                param_count += 1
            if request.GET.get("status", "") != '':
                if param_count > 0:
                    params += '&status=' + str(status)
                else:
                    params += '?status=' + str(status)
                param_count += 1
            if request.GET.get("show", "") != '':
                if param_count > 0:
                    params += '&show=' + str(show)
                else:
                    params += '?show=' + str(show)
                param_count += 1

            if request.GET.get("sort", "") != '':
                if param_count > 0:
                    params += '&sort=' + str(sort)
                else:
                    params += '?sort=' + str(sort)
                param_count += 1

            if param_count > 0:
                params += '&page='
            else:
                params += '?page='
                param_count += 1
            return render(request, 'staff_panel/users.html',{'users': users, 'users_count': users_count,'page_count': page_count, 'current_page': current_page, 'prev_page':prev_page, 'next_page': next_page, 'pages':pages, 'center_pages': center_pages, 'pp': pp, 'cc':cc,'show':show,'type': type,'status': status,'sort':sort, 'params': params,'is_search': True, 'search_text': search_text})
