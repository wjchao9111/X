"""
Django settings for X project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import

import os
import socket
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+=w^_me4ha#*-ey9ql%@k45$x28s0p*0+q9cj6o*q+yl)8mh55'

# SECURITY WARNING: don't run with debug turned on in production!

debugging = socket.gethostname() in ['Thinkpad', 'lenovo-PC']
DEBUG = debugging

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'X', 'base', 'addr', 'sms', 'filter', 'api','extra',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'X.tools.middleware.JsonMiddleware',
    'X.tools.middleware.AuthMiddleware',
    'X.tools.middleware.ExceptionMiddleware',
    'X.tools.middleware.HackHostMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'X.urls'

WSGI_APPLICATION = 'X.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# if debugging:
if debugging:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sms',
            'USER': 'root',
            'PASSWORD': 'hello',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'ATOMIC_REQUESTS': True,
        },
        'slave': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sms',
            'USER': 'root',
            'PASSWORD': 'hello',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'ATOMIC_REQUESTS': True,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sms',
            'USER': 'sms',
            'PASSWORD': '123456',
            'HOST': '111.11.84.251',
            'PORT': '3306',
            'ATOMIC_REQUESTS': True,
        },
        'slave': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sms',
            'USER': 'sms',
            'PASSWORD': '123456',
            'HOST': '111.11.84.252',
            'PORT': '3306',
            'ATOMIC_REQUESTS': True,
        }
    }
DATABASE_ROUTERS = ['X.tools.model.DBRouter']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'sms',
#         'USER': 'postgres',
#         'PASSWORD': 'hello',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMP_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = "X.tools.storage.FileStorage"

SESSION_COOKIE_AGE = 60 * 30
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

email_server = {'name': 'smtp.139.com', 'user': 'chaowang.sjz@139.com', 'passwd': 'Ff@000001'}

# Celery settings
BROKER_URL = 'redis://127.0.0.1:6379/0'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {

    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard',
        },
        'sql_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/sql.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
        'sms_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/sms.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
        'sms_error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/sms.error.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
        'task_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/task.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
        'filter_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/filter.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
        'common_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/common.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
        'spyne.application_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/spyne.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
        'celery_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/celery.log'),
            'when': 'MIDNIGHT',
            'backupCount': 180,
            'interval': 1,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'common_handler'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['sql_handler'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'sms': {
            'handlers': ['sms_handler', 'sms_error_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'task': {
            'handlers': ['task_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'filter': {
            'handlers': ['filter_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'common': {
            'handlers': ['common_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'spyne.application': {
            'handlers': ['spyne.application_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery': {
            'handlers': ['celery_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery.bootsteps': {
            'handlers': ['celery_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
