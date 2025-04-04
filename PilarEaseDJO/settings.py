"""
Django settings for PilarEaseDJO project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# settings.py

# settings.py
# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_performance_dashboard': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'performance_dashboard.log'),
        },
    },
    'loggers': {
        'admin_tools': {
            'handlers': ['file_performance_dashboard'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r&=lu-6-+chjserq1w2z%0kselz_^a7bxn@m%9vxs$4jhg&x4('

# SECURITY WARNING: don't run with debug turned on in production!
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
    'main', 
    'itrc_tools',
    'corsheaders',
    'debug_toolbar',
    'compressor',
    'import_export',
    'admin_tools.apps.AdminToolsConfig',
    'insights',
    'appointment.apps.AppointmentConfig',
    # 'channels',
]
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
AUTH_USER_MODEL = 'main.CustomUser'

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000/',
    'http://127.0.0.1:8000/'
]

LOGIN_URL = '/itrc/'  # or whatever your login URL is
LOGIN_REDIRECT_URL = '/itrc/dashboard/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# settings.py

AUTHENTICATION_BACKENDS = [
    'main.authentication_backends.CustomBackend',  # Replace 'your_app' with your actual app name
    # 'django.contrib.auth.backends.ModelBackend',  # Optionally keep the default backend
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',  # Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Ensure this is included
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'admin_tools.middleware.EmotionModelMiddleware',
    'main.middleware.TimezoneMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', 
]

# settings.py

USE_TZ = False
TIME_ZONE = 'Asia/Manila'


SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

INTERNAL_IPS = ['127.0.0.1']
# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # 30 minutes in seconds
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = 'PilarEaseDJO.urls'

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'main', 'templates'),
            os.path.join(BASE_DIR, 'admin_tools', 'templates'),
            os.path.join(BASE_DIR, 'itrc_tools', 'templates'),
            os.path.join(BASE_DIR, 'appointment', 'templates'),
            # Add other template directories if necessary
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # ... existing context processors ...
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'itrc_tools.context_processors.unread_notifications_count',  # Add this line
            ],
        },
    },
]

WSGI_APPLICATION = 'PilarEaseDJO.wsgi.application'

# ASGI_APPLICATION = 'PilarEaseDJO.asgi.application'

# # Set up the Channels layer (you can use Redis for production)
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],  # Make sure Redis is running on this host/port
#         },
#     },
# }

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pilarease_db',
        'USER': 'root',
        'PASSWORD': '',  # Add your MySQL root password if you have one, otherwise leave it empty
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        }
    }
}


import pymysql
pymysql.install_as_MySQLdb()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pilareasecounseling@gmail.com'
DEFAULT_FROM_EMAIL = 'pilareasecounseling@gmail.com'
EMAIL_HOST_PASSWORD = 'anlf kmbe xkqu pdbg'
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'admin_tools', 'static'),
    os.path.join(BASE_DIR, 'itrc_tools', 'static'),
    os.path.join(BASE_DIR, 'appointment', 'static'),
    # Add other static directories if necessary
]

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_OFFLINE = True

def get_hashed_css_files():
    css_dir = os.path.join(BASE_DIR, 'main', 'static', 'css')
    hashed_files = []
    if os.path.exists(css_dir):
        for file_name in os.listdir(css_dir):
            if file_name.startswith('main.') and file_name.endswith('.css'):
                hashed_files.append(f'css/{file_name}')
            elif file_name.startswith('custom.') and file_name.endswith('.css'):
                hashed_files.append(f'css/{file_name}')
    else:
        print(f"Directory does not exist: {css_dir}")
    return hashed_files


# Set hashed CSS files to be used in templates
HASHED_CSS_FILES = get_hashed_css_files()

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
