from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AmpoolAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ampool_auth'
    verbose_name = _('احراز هویت')