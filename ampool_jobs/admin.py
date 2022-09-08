from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    SupportersModel,
    DoctorModel, 
    TitleSkillModel, 
    DoctorDegreeModel,
    DoctorConsultingTimeModel,
    DoctorReservingTimeModel,
    MessagePermissionModel,
    MessageModel,
    TicketModel,
    ReportChatModel
)


class SupportersModel_Admin(admin.ModelAdmin):
    list_display = ['get_full_name', 'is_send_reply', 'is_create_blog', 'is_active']
    search_field = ['id']
    ordering = ['-user__id']

class DoctorModel_Admin(admin.ModelAdmin):
    list_display = ['get_full_name', 'is_advised', 'send_doctor_request_for_blogging', 'is_blogger', 'is_active']
    search_field = ['id', 'title']
    ordering = ['-user__id']

class TitleSkillModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class DoctorDegreeModel_Admin(admin.ModelAdmin):
    list_display = ['get_full_name', 'skill_title' , 'medical_system_code', 'is_valid']
    search_field = ['get_full_name']
    ordering = ['-id']

class DoctorConsultingTimeModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'day', 'time']
    search_field = ['day', 'time']
    ordering = ['-id']

class DoctorReservingTimeModel_Admin(admin.ModelAdmin):
    list_display = ['doctor_skill', 'patient', 'is_active']
    search_field = ['doctor_skill', 'patient']
    ordering = ['-id']

class MessagePermissionModel_Admin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'is_enabled']
    search_field = ['patient', 'doctor']
    ordering = ['-id']

class MessageModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']

class TicketModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'j_created']
    ordering = ['-id']

class ReportChatModel_Admin(admin.ModelAdmin):
    list_display = ['j_created']
    ordering = ['-id']

admin.site.register(SupportersModel, SupportersModel_Admin)
admin.site.register(DoctorModel, DoctorModel_Admin)
admin.site.register(TitleSkillModel, TitleSkillModel_Admin)
admin.site.register(DoctorDegreeModel, DoctorDegreeModel_Admin)
admin.site.register(DoctorConsultingTimeModel, DoctorConsultingTimeModel_Admin)
admin.site.register(DoctorReservingTimeModel, DoctorReservingTimeModel_Admin)
admin.site.register(MessagePermissionModel, MessagePermissionModel_Admin)
admin.site.register(MessageModel, MessageModel_Admin)
admin.site.register(TicketModel, TicketModel_Admin)
admin.site.register(ReportChatModel, ReportChatModel_Admin)