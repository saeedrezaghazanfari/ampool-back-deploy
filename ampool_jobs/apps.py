from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AmpoolJobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ampool_jobs'
    verbose_name = _('ماژول شغل ها')
