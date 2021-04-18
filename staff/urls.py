from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from . import views

urlpatterns = [
    path('main/', views.main, name='staff_main'),
    path('users/', views.users, name='staff_users'),
    path('user/<int:pk>/view/', views.user_view, name='staff_user_view'),
    path('user/<int:pk>/transactions/', views.user_transactions, name='staff_user_transactions'),
    path('user/<int:pk>/give/', views.user_give_etg, name='staff_user_give_etg'),
    path('user/<int:pk>/ips/', views.user_ips, name='staff_user_ips'),
    path('user/<int:pk>/referal/', views.user_percent, name='staff_user_referal'),
    path('finance_settings/', views.finance_settings, name='staff_finance_settings'),
    path('system_settings/', views.system_settings, name='staff_system_settings'),

    path('faqs/', views.faqs, name='staff_faqs'),
    path('faq/create/', views.faq_create, name='staff_faq_create'),
    path('faq/edit/<int:pk>/', views.faq_edit, name='staff_faq_edit'),

    path('news/', views.news, name='staff_news'),
    path('news/create/', views.news_create, name='staff_news_create'),
    path('news/edit/<int:pk>/', views.news_edit, name='staff_news_edit'),

    path('roadmap/', views.roadmap, name='staff_roadmap'),
    path('roadmap/create/', views.roadmap_create, name='staff_roadmap_create'),
    path('roadmap/edit/<int:pk>/', views.roadmap_edit, name='staff_roadmap_edit'),
]