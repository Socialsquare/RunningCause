# -*- coding: utf-8 -*-
"""
Django settings for RunningCause project.
"""

import os
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



BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
APP_URL = os.getenv('APP_URL')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# if os.getenv('DJANGO_SECRET_KEY'):
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
# else:
#     SECRET_KEY = 'BOGUS SECRET KEY -- CHANGE THIS'

# if os.getenv('RUNKEEPER_CLIENT_ID'):
RUNKEEPER_CLIENT_ID = os.getenv('RUNKEEPER_CLIENT_ID')
# else:
#     RUNKEEPER_CLIENT_ID = 'BOGUS CLIENT ID -- CHANGE THIS'

# if os.getenv('RUNKEEPER_CLIENT_SECRET'):
RUNKEEPER_CLIENT_SECRET = os.getenv('RUNKEEPER_CLIENT_SECRET')
# else:
#     RUNKEEPER_CLIENT_SECRET = 'BOGUS CLIENT SECRET -- CHANGE THIS'    
# RUNKEEPER_CLIENT_ID = secrets.RUNKEEPER_CLIENT_ID
# RUNKEEPER_CLIENT_SECRET = secrets.RUNKEEPER_CLIENT_SECRET

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

COURRIERS_MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
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
    'static_precompiler',
    'django.contrib.sites',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    #'allauth.socialaccount',
    'django_extensions',
    'Running',
    'jquery',
    'rosetta',
    'courriers',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Running.middleware.RedirectFromCnamesMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

AUTH_USER_MODEL = "Running.User"

LOGIN_REDIRECT_URL = '/sign_in_landing'
LOGIN_URL = '/signuporlogin'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SESSION_REMEMBER = None
USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_FORM_CLASS = 'Running.forms.SignupForm'


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


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Parse database configuration from $DATABASE_URL
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config(default=os.environ.get('DATABASE_URL'))



LANGUAGES = (
    # ('en', _('English')),
    ('da', _('Danish')),
    )

LANGUAGE_CODE = 'da-dk'


SITE_ID = 1
SITE_DOMAIN = 'runners.masanga.dk'
BASE_URL = 'http://' + SITE_DOMAIN

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

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "allauth.account.context_processors.account",
    #"allauth.socialaccount.context_processors.socialaccount",

)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'static_precompiler.finders.StaticPrecompilerFinder',
)


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
#from django.contrib.sites.models import Site
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

