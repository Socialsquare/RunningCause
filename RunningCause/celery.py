from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RunningCause.settings')

from django.template import loader, Context
from django.conf import settings

app = Celery('RunningCause')
app.config_from_object('RunningCause.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
