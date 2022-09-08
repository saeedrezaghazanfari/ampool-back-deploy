from django.db import models
from django.utils.translation import gettext_lazy as _
from ampool_auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Extentions.utils import doctor_degree_path, file_chat_path, jalali_convertor, ticket_image_path


class SupportersModel(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    is_send_reply = models.BooleanField(default=False, verbose_name=_('اجازه‌ی ارسال پاسخ به کاربران'))
    is_create_blog = models.BooleanField(default=False, verbose_name=_('اجازه‌ی تولید پست'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال / غیرفعال'))
    
    class Meta:
        ordering = ['-user__id']
        verbose_name = _('پشتیبان')
        verbose_name_plural = _('پشتیبانان')

    def __str__(self):
        return str(self.user.get_full_name())

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام پشتیبان')


class DoctorModel(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    history = models.TextField(blank=True, null=True, verbose_name=_('سابقه ی پزشکی'))
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('بیوگرافی'), help_text=_('این متن در زمان ارائه‌ی مقالات پزشکی شما در سایت، به کاربران نشان داده خواهد شد'))
    is_advised = models.BooleanField(default=False, verbose_name=_('اجازه برای مشاوره دادن به بیماران'), help_text=_('اگر این گزینه فعال این پزشک میتواند برنامه‌ی پزشکی تعیین کند و وقت مشاوره ارائه بدهد'))
    send_doctor_request_for_blogging = models.BooleanField(default=False, verbose_name=_('درخواست وبلاگنویسی'), help_text=_('آیا این پزشک درخواست برای بلاگنویسی داده است؟'))
    is_blogger = models.BooleanField(default=False, verbose_name=_('نویسنده است؟'), help_text=_('اجازه‌ی نوشتن مقالات'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال / غیرفعال'))

    class Meta:
        ordering = ['-user__id']
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشک ها')

    def __str__(self):
        return str(self.user.get_full_name())

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام پزشک')


class TitleSkillModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('عنوان تخصص'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عنوان تخصص')
        verbose_name_plural = _('عناوین تخصص‌ها')

    def __str__(self):
        return self.title


class DoctorDegreeModel(models.Model):
    DATE_MONTH_TUPLE = (('1', _('فروردین')), ('2', _('اردیبهشت')), ('3', _('خرداد')), ('4', _('تیر')), ('5', _('مرداد')), ('6', _('شهریور')), ('7', _('مهر')), ('8', _('آبان')), ('9', _('آذر')), ('10', _('دی')), ('11', _('بهمن')), ('12', _('اسفند')), )
    doctor = models.ForeignKey(DoctorModel, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    score = models.PositiveIntegerField(default=0, verbose_name=_('امتیاز'))
    skill_title = models.ForeignKey(TitleSkillModel, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('عنوان تخصص/ها'))
    degree_image = models.ImageField(upload_to=doctor_degree_path, null=True, blank=True, verbose_name=_('تصویر مدرک'))
    # info of degree
    medical_system_code = models.IntegerField(blank=True, null=True, verbose_name=_('کد نظام پزشکی'))
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('نام'))
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('نام خانوادگی'))
    father_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('نام پدر'))
    birth_certificate_id = models.BigIntegerField(blank=True, null=True, verbose_name=_('شماره شناسنامه'))
    national_code = models.BigIntegerField(blank=True, null=True, verbose_name=_('کدملی'))
    issued_from = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('صادره از'))
    degree_date = models.DateField(blank=True, null=True, verbose_name=_('تاریخ صدور'))
    average = models.FloatField(blank=True, null=True, verbose_name=_('معدل'))
    average_chars = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('معدل با حروف'))
    medical_field_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('نام رشته'))
    is_valid = models.BooleanField(default=False, verbose_name=_('فعال / غیرفعال'), help_text=_('آیا این مدرک تایید شده است؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تخصص پزشک')
        verbose_name_plural = _('تخصص ‌های پزشکان')
    
    def __str__(self):  
        return f'{self.doctor.user.first_name} {self.doctor.user.last_name} ({self.skill_title})'

    def get_full_name(self):
        return f'{self.doctor.user.first_name} {self.doctor.user.last_name}'
    get_full_name.short_description = _('نام پزشک')
    


class DoctorConsultingTimeModel(models.Model):
    DAYS = (
        ('saturday', _('شنبه')),
        ('sunday', _('یک شنبه')),
        ('monday', _('دو شنبه')),
        ('tuesday', _('سه شنبه')),
        ('wednesday', _('چهار شنبه')),
        ('thursday', _('پنج شنبه')),
        ('friday', _('جمعه')),
    )
    TIMES = (
        ('6-8', '6-8'),
        ('8-10', '8-10'),
        ('10-12', '10-12'),
        ('12-14', '12-14'),
        ('14-16', '14-16'),
        ('16-18', '16-18'),
        ('18-20', '18-20'),
    )
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    skill = models.ManyToManyField(DoctorDegreeModel, verbose_name=_('تخصص‌ها'))
    day = models.CharField(max_length=15, blank=True, null=True, choices=DAYS, verbose_name=_('روز'))
    time = models.CharField(max_length=15, blank=True, null=True, choices=TIMES, verbose_name=_('زمان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان مشاوره‌ی پزشک')
        verbose_name_plural = _('زمان‌های مشاوره‌ی پزشک')
    
    def __str__(self):  
        return self.doctor.user.first_name + ' ' + self.doctor.user.last_name


class DoctorReservingTimeModel(models.Model):
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    doctor_skill = models.ForeignKey(DoctorDegreeModel, on_delete=models.CASCADE, verbose_name=_('تخصص پزشک'))
    patient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('بیمار'))
    requestedtime_day = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('روز درخواستی از سمت بیمار'))
    requestedtime_time = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('ساعت درخواستی از سمت بیمار'))
    is_doctor_see = models.BooleanField(default=False, verbose_name=_('آیا پزشک این درخواست را مشاهده کرده است؟'))
    visit_date = models.DateField(blank=True, null=True, verbose_name=_('تاریخ ملاقات با دکتر'))
    visit_timefrom = models.TimeField(blank=True, null=True, verbose_name=_('زمان ملاقات با دکتر از'))
    visit_timeto = models.TimeField(blank=True, null=True, verbose_name=_('زمان ملاقات با دکتر تا'))
    is_active = models.BooleanField(default=False, verbose_name=_('آیا این زمان رزرو شده است؟'))
    is_ended = models.BooleanField(default=False, verbose_name=_('آیا این ملاقات به اتمام رسیده است؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان ملاقات پزشک')
        verbose_name_plural = _('زمان‌های ملاقات پزشک')
    
    def __str__(self):  
        return self.doctor.user.first_name + ' ' + self.doctor.user.last_name


class MessagePermissionModel(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('بیمار'))
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    skill = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('تخصص پزشک'))
    is_enabled = models.BooleanField(default=False, verbose_name=_('فعال بودن چت'))
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('اجازه‌ی چت')
        verbose_name_plural = _('اجازه‌ی چت‌ها')
    
    def __str__(self):  
        return str(self.id)


class MessageModel(models.Model):
    msg_permission = models.ForeignKey(MessagePermissionModel, on_delete=models.CASCADE, verbose_name=_('اجازه‌ی چت'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('پاسخ'))
    sender = models.ForeignKey(User, related_name='msg_sender', on_delete=models.CASCADE, verbose_name=_('فرستنده'))
    receiver = models.ForeignKey(User, related_name='msg_receiver', on_delete=models.CASCADE, verbose_name=_('گیرنده'))
    msg = models.TextField(blank=True, null=True, verbose_name=_('متن پیام'))
    file = models.FileField(upload_to=file_chat_path, null=True, blank=True, verbose_name=_('فایل'))
    is_send = models.BooleanField(default=False, verbose_name=_('فرستاده شد؟'))
    is_seen = models.BooleanField(default=False, verbose_name=_('دیده شد؟'))
    is_reply = models.BooleanField(default=False, verbose_name=_('آیا این پیام پاسخ میباشد؟'))
    have_file = models.BooleanField(default=False, verbose_name=_('آیا این پیام شامل فایل میباشد؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = _('چت')
        verbose_name_plural = _('چت ها')
    
    def __str__(self):  
        return str(self.id)


class TicketModel(models.Model):
    DEPARTMENT_CHOICES = (
        ('finance', _('Finance and Administration')), 
        ('ac_activation', _('Account Activation')), 
        ('ac_upgrade', _('Upgrade Account')), 
        ('webSite_performance', _('WebSite Performance')), 
        ('other', _('Other'))
    )
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('پاسخ'))
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    department = models.CharField(max_length=100, blank=True, null=True, choices=DEPARTMENT_CHOICES, verbose_name=_('دپارتمان'))
    subject = models.CharField(max_length=225, blank=True, null=True, verbose_name=_('عنوان'))
    content = models.TextField(verbose_name=_('محتوا'))
    image = models.ImageField(upload_to=ticket_image_path, null=True, blank=True, verbose_name=_('تصویر'))
    is_read_user = models.BooleanField(default=False, verbose_name=_('خوانده شده توسط کاربر؟'))
    is_read_supporter = models.BooleanField(default=False, verbose_name=_('خوانده شده توسط پشتیبان؟'))
    is_reply = models.BooleanField(default=False, verbose_name=_('آیا این تیکت پاسخ است؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت ها')
    
    def __str__(self):  
        return str(self.id)
    
    def j_created(self):
        return jalali_convertor(self.created, 'date_time')
    j_created.short_description = _('تاریخ گزارش')

class ReportChatModel(models.Model):
    reporter = models.ForeignKey(User, related_name='reporter_chat', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('گزارش کننده'))
    reported = models.ForeignKey(User, related_name='reported_chat', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('گزارش شده'))
    report_type = models.CharField(max_length=255, verbose_name=_('نوع گزارش'))
    created = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False, verbose_name=_('رسیدگی شده است؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گزارش')
        verbose_name_plural = _('گزارش ها')
    
    def __str__(self):  
        return str(self.id)
    
    def j_created(self):
        return jalali_convertor(self.created, 'date_time')
    j_created.short_description = _('تاریخ گزارش')


# signals
@receiver(post_save, sender=SupportersModel)
def save_is_supporter_in_USER_model(sender, instance, created, **kwargs):
    if instance.is_active:
        user = User.objects.get(username=instance.user.username)
        user.is_supporter = True
        user.save()