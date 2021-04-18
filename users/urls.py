from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from . import views

urlpatterns = [
    path('auth/login/', views.signin, name='client_signin'),
    path('auth/registration/', views.signup, name='client_signup'),
    path('auth/logout/', views.signout, name='client_sigout'),
    path('auth/recovery/', views.pass_recovery, name='client_pass_recovery'),
    path('account/settings/', views.settings_redirect, name='client_settings_redirect'),
    path('account/settings/general/', views.settings_general, name='client_settings'),
    path('account/settings/partners/', views.settings_partners, name='client_settings_partners'),

    path('verify/<slug:code>/', views.verify_email, name='client_verify_email'),
    path('recovery/<slug:code>/', views.recovery, name='client_recovery'),
]