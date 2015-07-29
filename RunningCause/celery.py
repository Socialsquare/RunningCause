from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RunningCause.settings')

from django.conf import settings

app = Celery('RunningCause')
app.config_from_object('RunningCause.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task()
def add(x, y):
    """
    Test task `add`
    """
    return x + y
