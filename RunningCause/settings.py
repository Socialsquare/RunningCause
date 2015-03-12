"""
Django settings for RunningCause project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# import secrets
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


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

SITE_ID = 1

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
    'allauth.socialaccount',
    'django_extensions',
    'Running',
    'jquery',
    'rosetta',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

AUTH_USER_MODEL = "Running.User"

LOGIN_REDIRECT_URL = '/sign_in_landing'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True

ACCOUNT_SIGNUP_FORM_CLASS = 'Running.forms.SignupForm'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.getenv('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.getenv('MAILGUN_SMTP_PORT')

SOCIALACCOUNT_QUERY_EMAIL = False

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


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s

LANGUAGES = (
    ('en', ugettext('English')),
    ('da', ugettext('Danish')),
    )

BASE_DOMAIN = 'http://masanga-runners.herokuapp.com/'

TIME_ZONE = 'Europe/Copenhagen'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale')+"/",
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.contrib.auth.context_processors.auth",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",

)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/



STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'static_precompiler.finders.StaticPrecompilerFinder',
)


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
#from django.contrib.sites.models import Site
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
