from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main.panel_redirect, name="client_panel_redirect"),
    path('wallet/', views.main.index, name="client_main"),
    path('wallet/buy/', views.main.buy, name="client_buy"),
    path('partners/', views.main.team, name="client_team"),
    path('staking/', views.main.staking, name="client_staking"),
]