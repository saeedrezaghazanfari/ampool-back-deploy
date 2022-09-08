from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AmpoolWebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ampool_website'
    verbose_name = _('ماژول های وبسایت')
