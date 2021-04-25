from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from .views import *

urlpatterns = [
    path('faqs/all/', FaqListView.as_view()),
    path('faq/<int:pk>/', FaqView.as_view()),
]