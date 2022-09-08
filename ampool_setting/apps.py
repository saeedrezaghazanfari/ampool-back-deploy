from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AmpoolSettingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ampool_setting'
    verbose_name = _('تنظیمات')