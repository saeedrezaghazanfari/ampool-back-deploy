from django.contrib import admin
from .models import (
    SettingModel,
    SendSMSModel,
    ConsultingPriceRateModel,
    UserActionsModel
)


class SettingModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']

class SendSMSModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'is_send']
    ordering = ['-id']

class ConsultingPriceRateModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']

class UserActionsModel_Admin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'j_created']
    ordering = ['-id']


admin.site.register(SettingModel, SettingModel_Admin)
admin.site.register(SendSMSModel, SendSMSModel_Admin)
admin.site.register(ConsultingPriceRateModel, ConsultingPriceRateModel_Admin)
admin.site.register(UserActionsModel, UserActionsModel_Admin)