"""
Django settings for RaPo3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from core.cf import conf

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=j@x-nxs&ipqx0j(g3j@i*3hvi27qtp!1715his4=@o1cs&1h+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

HOST = 'http://localhost:8000'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # 'django_seo_js',
    'api',
    'myadmin',
    'myguest',
    'static_site',
    'core',
    'weapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django_seo_js.middleware.EscapedFragmentMiddleware',  # If you're using #!
    # 'django_seo_js.middleware.UserAgentMiddleware',  # If you want to detect by user agent
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'core.middleware.ExceptCaptureMiddleware',
)

# SEO_JS_PRERENDER_TOKEN = ""
#
# SEO_JS_USER_AGENTS = [
#     "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
# ]

ROOT_URLCONF = 'RaPo3.urls'

WSGI_APPLICATION = 'RaPo3.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': conf.rapo_db_name,
        'USER': conf.rapo_user,  # Not used with sqlite3.
        'PASSWORD': conf.rapo_password,  # Not used with sqlite3.
        'HOST': conf.rapo_host,  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': conf.rapo_port,
    }
}

sentry_sdk.init(
    dsn="https://02d4c64a8e0c4d528362f7ee766ac5d8@o73389.ingest.sentry.io/158073",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_MEDIA = './static/'

STATIC_ROOT = './static/'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

# email

EMAIL_HOST = 'smtp.163.com'

EMAIL_PORT = 25

EMAIL_HOST_USER = 'bluedazzle@163.com'

EMAIL_HOST_PASSWORD = ''

DEFAULT_CHARSET = 'utf-8'
