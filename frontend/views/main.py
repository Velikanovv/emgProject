from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import logout
from users.models import *
from finance.models import *
from finance.services import buyETG_PayByUsd
from decimal import Decimal

def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            history = TransactionHistory.objects.filter(transaction_history_user=user).order_by('-date').all()
            if len(history) > 15:
                history = history[:15]
            return render(request, 'client_panel/wallet.html',{'history': history })

def buy(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'client_panel/buy.html',{})
        elif request.method == 'POST':
            if 'action' in request.POST:
                if request.POST['action'] == 'buy-etg':
                    count = request.POST['count']
                    try:
                        buyETG_PayByUsd(user=user, count=Decimal(count))
                        return JsonResponse({}, status=200)
                    except Exception as e:
                        return JsonResponse({'errors': e.args[0]}, status=400)

def team(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            actions = ReferalsAdded.objects.filter(referal_card=user.referal_card).order_by('-date').all()
            if len(actions) > 8:
                actions = actions[8]
            return render(request, 'client_panel/team.html', {'last_actions': actions})

def staking(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('landing_main')
    if user.is_authenticated:
        if request.method == 'GET':
            etg_history = StakingETGHistory.objects.filter(balance=user.balance_etg).order_by('-date')
            etggold_history = StakingETGGOLDHistory.objects.filter(balance=user.balance_etggold).order_by('-date')
            if len(etg_history) > 10:
                etg_history = etg_history[:10]
            if len(etggold_history) > 10:
                etggold_history = etggold_history[:10]
            return render(request, 'client_panel/staking.html', {'etg_history': etg_history, 'etggold_history': etggold_history})

def panel_redirect(request):
    return redirect('client_main')