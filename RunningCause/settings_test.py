import sys
from .settings import *


STATICFILES_STORAGE = ''

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SECRET_KEY = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*', ]

INSTALLED_APPS += ('django_nose', )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
     '--verbosity=2',
     '--with-yanc',
     '--cover-branches',
     '--with-coverage',
     '--cover-erase',
     '--cover-package=common',
     '--cover-package=invitations',
     '--cover-package=pages',
     '--cover-package=payments',
     '--cover-package=profile',
     '--cover-package=RunningCause',
     '--cover-package=runs',
     '--cover-package=sponsorship',
     '--cover-package=wagers',
]

for arg in sys.argv:
    if arg.startswith('--tests='):
        NOSE_ARGS = [
            '--verbosity=2',
            '--stop',
            '--with-yanc',
        ]
        break
