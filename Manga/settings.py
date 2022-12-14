"""
Django settings for Manga project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

prod =os.environ.get("PROD", default=False)
prod_db = os.environ.get("PROD_DB", default=False)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if prod:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = int(os.environ.get("DEBUG", default=0))
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
    DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }
    STATIC_URL = "static/"
    #STATIC_ROOT = os.path.join(BASE_DIR, '/static') 
    STATIC_ROOT = BASE_DIR / "static"
    STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/home/app/www/static/',
]
else:
    SECRET_KEY = 'django-insecure-!esofi1&pwf4k^myj5ac3o*r7_qe!0-^*jd1nyqhlzmriduh4k'
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', '*']
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'manga',
        'USER': 'mangauser',
        'PASSWORD': '31467539',
        'HOST': '192.168.1.111',
        'PORT': '49153',
        #'PORT': '49160',
        }
    }
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, '/static')
    if prod_db:
        DATABASES['default']['PORT'] = '49160'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

#STATICFILES_DIRS = ( os.path.join('static'), )


# SECURITY WARNING: don't run with debug turned on in production!




# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Core',
    'UserProfile',
    #'MyUser',
    #"django.contrib.staticfiles",
    "debug_toolbar",
    'django_extensions',
    'corsheaders',
]

CORS_ORIGIN_ALLOW_ALL=True
CORS_ORIGIN_WHITELIST = [
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'UserProfile.middleware.SimpleMiddleware',
    'UserProfile.middleware.simple_middleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'Manga.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'UserProfile.context_processors.settings',
            ],
        },
    },
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'
# STATICFILES_DIRS = ( os.path.join('static'), )

WSGI_APPLICATION = 'Manga.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'manga',
#        'USER': 'mangauser',
#        'PASSWORD': '31467539',
#        'HOST': '192.168.1.105',
#        'PORT': '5432',
#    }
#}


# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
#         "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
#         "USER": os.environ.get("SQL_USER", "user"),
#         "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
#         "HOST": os.environ.get("SQL_HOST", "localhost"),
#         "PORT": os.environ.get("SQL_PORT", "5432"),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(SETTINGS_PATH, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

#STATIC_URL = 'static/'


#
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
}

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

REDIS_HOST = os.environ.get('REDIS_HOST', default='localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', default='49154')
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
if os.environ.get('PROD', default=0):
    CELERY_RESULT_BACKEND = "redis://redis:6379"
    BROKER_URL = "redis://redis:6379"
else:
    CELERY_RESULT_BACKEND = 'redis://default:redispw@' + REDIS_HOST + ':' + REDIS_PORT
    BROKER_URL = 'redis://default:redispw@' + REDIS_HOST + ':' + REDIS_PORT