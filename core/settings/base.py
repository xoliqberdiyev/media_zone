from pathlib import Path
import os, environ

env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

LOCAL_APPS = [
    'apps.shared',
    'apps.authentication',
    'apps.finance',
    'apps.client',
    'apps.estimate',
    'apps.rooms',
    'apps.web',
]

THIRD_PARTY_PACKAGES = [
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'storages',
]

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += THIRD_PARTY_PACKAGES
INSTALLED_APPS += LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'resources/static/'
STATIC_ROOT = BASE_DIR / 'resources/static'

MEDIA_URL = "https://1477816.servercore.cloud/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.User'

DEFAULT_FILE_STORAGE="storages.backends.s3boto3.S3Boto3Storage"


from core.packages.jazzmin import *
from core.packages.swagger import *
from core.packages.rest_framework import *
from core.packages.simlejwt import *
from core.packages.cors_headers import *
from core.conf.logs import LOGGING
# from core.packages.s3 import *

LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)
MODELTRANSLATION_LANGUAGES = ('ru', 'uz')

AWS_ACCESS_KEY_ID='ab13231c33604420851f3288a805703b'
AWS_SECRET_ACCESS_KEY='342f429e1fb04f2e86959dc6c83b0c54'
AWS_STORAGE_BUCKET_NAME='medias'
AWS_S3_ENDPOINT_URL='https://s3.uz-2.srvstorage.uz'
AWS_S3_REGION_NAME="uz-2"
AWS_S3_FILE_OVERWRITE=False
AWS_QUERYSTRING_AUTH=False
AWS_DEFAULT_ACL="public-read"
AWS_S3_CUSTOM_DOMAIN='8d030fad-5687-4157-adf9-d7d72d42d14a.srvstatic.uz'
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
#     "ContentType": "image/jpeg",  # faqat jpg uchun
# }
DEFAULT_FILE_STORAGE = 'services.storage.storage_backend.MediaStorage'
