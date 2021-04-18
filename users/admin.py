from .models import UserIP, UserPhoneNumber, User, ReferalCard, ReferalsAdded, RecoveryCode
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.sessions.models import Session
...


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password','ip','role')}),
        (_('Personal info'), {'fields': ('name', 'surname','patronymic','phone_number')}),
        (_('Balance info'), {'fields': ('balance_etg', 'balance_usd','transaction_history')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_banned','is_email_verified')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined','next_email_verify_send')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'surname', 'is_staff')
    search_fields = ('email', 'name', 'surname')
    ordering = ('-date_joined',)

admin.site.register(Session)
admin.site.register(UserIP)
admin.site.register(UserPhoneNumber)
admin.site.register(ReferalCard)
admin.site.register(ReferalsAdded)
admin.site.register(RecoveryCode)