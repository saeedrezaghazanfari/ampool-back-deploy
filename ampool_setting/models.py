from django.db import models
from django.forms import ChoiceField
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from Extentions.utils import jalali_convertor
from ampool_auth.models import User

class SettingModel(models.Model):
    x_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایکس'))
    y_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایگرگ'))
    marker_text = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('متن شما روی نقشه'))
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('کشور'))
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('استان'))
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('شهرستان'))
    phone = models.PositiveBigIntegerField(verbose_name=_('تلفن'))
    from_to = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('زمان گشایش'))
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=_('ایمیل'))
    your_text = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('متن شما درمورد ارتباط'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('‌تنظیمات')
        verbose_name_plural = _('‌تنظیمات')

    def __str__(self):
        return str(_('شما حتما باید یک مقدار در این جدول ذخیره کنید.'))


class SendSMSModel(models.Model):
    RECIEVERS = (('all', _('همه')), ('patients', _('بیماران')), ('doctors', _('پزشک‌ها')), ('nurses', _('پرستاران')))
    title = models.CharField(max_length=255, verbose_name=_('عنوان پیامک'), help_text=_('این مقدار فقط در دیتابیس میباشد و برای کاربر ارسال نمیشود'))
    content = models.TextField(verbose_name=_('متن پیامک'))
    recievers = models.CharField(max_length=20, choices=RECIEVERS, default='all', verbose_name=_('چه کسانی این پیامک را دریافت کنند؟'))
    is_send = models.BooleanField(default=False, verbose_name=_('ارسال شود؟'), help_text=_('اگر این گزینه فعال شد و این رکورد را ذخیره کردید، بلافاصله ارسال پیامک آغاز میشود.'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('پیامک پزشکی')
        verbose_name_plural = _('پیامک‌های پزشکی')

    def __str__(self):
        return self.title


class ConsultingPriceRateModel(models.Model):
    time = models.IntegerField(default=5, verbose_name=_('تایم ابتدایی'))
    price = models.FloatField(default=50000, verbose_name=_('نرخ ابتدایی - تومان'))
    price_2 = models.FloatField(default=25000, verbose_name=_('نرخ پیج دقیقه‌ی اضافه - تومان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نرخ مشاوره')
        verbose_name_plural = _('نرخ مشاوره')

    def __str__(self):
        return str(_('شما حتما باید یک مقدار در این جدول ذخیره کنید.'))


class UserActionsModel(models.Model):
    ACTION_TYPE = (
        ('financial', _('امور مالی')), 
        ('medical_advice', _('مشاوره‌ی پزشکی')), 
        ('recommender', _('توصیه گر')),
        ('upgrade_ac', _('ارتقای حساب کاربری')),
        ('change_pw', _('تغییر رمزعبور')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    action_type = models.CharField(max_length=255, default='financial', choices=ACTION_TYPE, verbose_name=_('نوع اقدام'))
    action = models.TextField(blank=True, null=True, verbose_name=_('شرح اقدام انجام شده'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('اقدام کاربر')
        verbose_name_plural = _('اقدامات کاربران')

    def j_created(self):
        return jalali_convertor(self.created, 'date_time')
    j_created.short_description = _('زمان و تاریخ')

    def __str__(self):
        return str(self.user)


# signals
## send sms to users

@receiver(post_save, sender=SendSMSModel)
def send_sms_to_uses(sender, instance, created, **kwargs):
    if instance.is_send:
        print('send sms is started!!!!!!!')
        # send SMS #TODO
        # check the is_send_sms of users