from pathlib import Path
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-e!i@fu@d)$(@5d52_3x9$%#@y$+o4cksb+y@eza6m$lws-fdy-'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'ampool_auth.apps.AmpoolAuthConfig',
    'ampool_website.apps.AmpoolWebsiteConfig',
    'ampool_setting.apps.AmpoolSettingConfig',
    'ampool_jobs.apps.AmpoolJobsConfig',

    # Packs
    'widget_tweaks',
    'captcha',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',   # add for translating
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'App_Config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'App_Config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
    ('ar', _('Arabic')),
]
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/site_static/'
STATIC_ROOT = Path("static_cdn", "static_root")
MEDIA_URL = '/media/'
MEDIA_ROOT = Path("static_cdn", "media_root")
STATICFILES_DIRS = [ Path("assets") ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# custom user
AUTH_USER_MODEL = 'ampool_auth.User'
LOGIN_URL = '/fa/sign-in'

# captcha
CAPTCHA_FONT_SIZE = 30
CAPTCHA_BACKGROUND_COLOR = '#fff'
CAPTCHA_FOREGROUND_COLOR = '#4f98dc'
CAPTCHA_LENGTH = 4
CAPTCHA_IMAGE_SIZE = (100, 50) 
