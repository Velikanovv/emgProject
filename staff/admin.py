from django.contrib import admin

# Register your models here.
from .models import SystemSettings
from solo.admin import SingletonModelAdmin


admin.site.register(SystemSettings)