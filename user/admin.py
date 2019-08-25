from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from exchange.models import UserBalance, BalanceHistory
from user.models import User


class UserBalanceInline(admin.TabularInline):
    model = UserBalance
    fields = ('coin', 'balance')
    extra = 0

class BalanceHistoryInline(admin.TabularInline):
    model = BalanceHistory
    fields = ('coin', 'amount', 'modification_type', 'created_at', 'payment_address', 'modified_by_user')
    readonly_fields = ('coin', 'amount', 'modification_type', 'created_at', 'payment_address', 'modified_by_user')
    fk_name = 'user'
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = (UserBalanceInline, BalanceHistoryInline)


admin.site.register(User, CustomUserAdmin)
