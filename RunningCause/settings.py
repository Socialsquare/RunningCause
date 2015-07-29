# coding: utf8
"""
Django settings for RunningCause project.
"""

import os
from os.path import dirname, abspath
import dj_database_url
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as messages_constants

ADMINS = (
    ('admin', 'pawel+runners-prod@socialsquare.dk'),
)

MANAGERS = (
    ('Paweł Bielecki', 'pawel+runners-prod-manager@socialsquare.dk'),
)

MESSAGE_TAGS = {
    messages_constants.ERROR: 'danger',
}

PROJECT_DIR = dirname(abspath(__file__))
BASE_DIR = dirname(PROJECT_DIR)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')


RUNKEEPER_CLIENT_ID = os.getenv('RUNKEEPER_CLIENT_ID', '')
RUNKEEPER_CLIENT_SECRET = os.getenv('RUNKEEPER_CLIENT_SECRET')

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')

COURRIERS_MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
COURRIERS_MAILCHIMP_LIST = '2640511eac'

DEBUG = False

TEMPLATE_DEBUG = DEBUG

# Application definition

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'widget_tweaks',
    'django_redis',
    'allauth',
    'allauth.account',
    #'allauth.socialaccount',
    'django_extensions',
    'bootstrap3',
    'rosetta',
    'courriers',

    'profile',
    'runs',
    'sponsorship',
    'wagers',
    'invitations',
    'tools',
    'pages',
    'payments',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'RunningCause.middleware.RedirectFromCnamesMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

AUTH_USER_MODEL = "profile.User"

LOGIN_REDIRECT_URL = '/profile/sign_in_landing'
LOGIN_URL = '/profile/signuporlogin'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SESSION_REMEMBER = None
USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_FORM_CLASS = 'profile.forms.SignupForm'


EMAIL_SUBJECT_PREFIX = '[Masanga Runners] '
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.getenv('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.getenv('MAILGUN_SMTP_PORT')
DEFAULT_FROM_EMAIL = 'masangarunners@masanga.dk'

SOCIALACCOUNT_QUERY_EMAIL = False

COURRIERS_BACKEND_CLASS = 'courriers.backends.mailchimp.MailchimpBackend'
COURRIERS_DEFAULT_FROM_NAME = 'masanga'

SOCIALACCOUNT_PROVIDERS = {
    # 'facebook': {
    #     'SCOPE': ['email', 'publish_stream'],
    #     'METHOD': 'js_sdk'
    # }
}

ROOT_URLCONF = 'RunningCause.urls'

WSGI_APPLICATION = 'RunningCause.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(default=os.environ.get('DATABASE_URL'))


REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,  # in seconds
            'SOCKET_TIMEOUT': 5,  # in seconds
        }
    }
}


LANGUAGES = (
    ('en', _('English')),
    ('da', _('Danish')),
)

LANGUAGE_CODE = 'da-dk'


SITE_ID = 1
SITE_DOMAIN = 'runners.masanga.dk'
BASE_URL = 'http://' + SITE_DOMAIN
APP_URL = os.getenv('APP_URL')

TIME_ZONE = 'Europe/Copenhagen'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale')+"/",
)

TEMPLATE_DIRS = [
    os.path.join(os.path.dirname(__file__), 'templates'),
]

CTX_PROCESSORS_TUPLE = (
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.template.context_processors.static",
    "django.template.context_processors.media",
    "RunningCause.context_processors.base_url",
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': CTX_PROCESSORS_TUPLE,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = [SITE_DOMAIN, ]

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  [%(name)s:%(lineno)s]  %(levelname)s - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'RunningCause': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'invitations': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'pages': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'payments': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'profile': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'runs': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'sponsorship': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'tools': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'wagers': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'celery': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
    }
}
