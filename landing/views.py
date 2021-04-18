from django.shortcuts import render, redirect, reverse
from users.models import UserIP, ReferalCard
from django.utils import timezone

# Create your views here.

def referal_url(request, ref_code):
    user = request.user
    print(request.META)
    if not user.is_authenticated:
        if request.method == 'GET' and ReferalCard.objects.filter(referal_code=ref_code).exists():
            request.session['ref_code'] = ref_code
            return redirect('landing_main')
        else:
            return redirect('landing_main')
    else:
        return redirect('landing_main')

def landing_main(request):
    if request.method == 'GET':
        ref_code = request.GET.get("ref", "")
        if ReferalCard.objects.filter(referal_code=ref_code).exists() and ref_code != "" and not request.user.is_authenticated:
            request.session['ref_code'] = ref_code
        return render(request, 'landing/index.html',{})