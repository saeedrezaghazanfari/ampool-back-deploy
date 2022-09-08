from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, LoginCodeModel


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] = (
        'first_name',
        'last_name',
        'phone',
        'profile',
        'wallet_balance',
        'visit_free_times',
        'gender',
        'age',
        'weight',
        'height',
        'address',
        'location_x',
        'location_y',
        'is_send_sms',
        'is_active2',
        'is_doctor',
        'is_supporter'
    )
    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'is_staff',
        'is_superuser',
        # 'groups',
        # 'user_permissions',
    )
    list_display = ('id', 'username', 'get_full_name', 'phone', 'gender')
    ordering = ['-id']

class LoginCodeModel_A(admin.ModelAdmin):
    list_display = ['user', 'code', 'j_date', 'j_expire', 'is_use']
    search_field = ['is_use', 'user']
    ordering = ['-id']



admin.site.register(User, AdminUser)
admin.site.register(LoginCodeModel, LoginCodeModel_A)
admin.site.unregister(Group)          # hide groups