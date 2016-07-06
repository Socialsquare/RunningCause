from .base import *

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'kraen@socialsquare.dk'
EMAIL_HOST_PASSWORD = 'jxzfqgdifixeirhy'

SECRET_KEY = 'you-will-never-guess-this'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_widECDRawLUD2VTdAGWAjv2i')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_xo9viXx96fMhQ4HaNYvPIT86')

SITE_DOMAIN = 'localhost:8000'
BASE_URL = 'http://' + SITE_DOMAIN
