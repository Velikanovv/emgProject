from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from . import views

urlpatterns = [
    path('', views.landing_main, name='landing_main'),
    path('r/<slug:ref_code>', views.referal_url, name='referal_url'),
]