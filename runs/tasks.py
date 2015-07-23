# coding: utf8
from __future__ import absolute_import

import logging
import datetime
from datetime import time, timedelta

from dateutil.parser import parse
import requests
from celery import shared_task

from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, Context

from .runkeeper import create_runs_from_runkeeper


log = logging.getLogger(__name__)


@shared_task(name='add')
def add(x, y):
    """
    Test task `add`
    """
    return x + y


@shared_task(name='pull_user_runs_from_runkeeper', ignore_result=True)
def pull_user_runs_from_runkeeper(user_id=None):
    create_runs_from_runkeeper(user_id=user_id)


@shared_task(name='notify_sponsors_about_run', ignore_result=True)
def notify_sponsors_about_run(run_id=None):
    """
    Notify sponsors about the run
    """
    from runs.models import Run
    run = Run.objects.get(id=run_id).select_related('runner')
    runner = run.runner
    relevant_sponsors = runner.sponsorships_recieved\
        .filter(end_date__gte=run.start_date, start_date__lte=run.start_date)\
        .exclude(sponsor__isnull=True)\
        .distinct('sponsor')

    relevant_emails = relevant_sponsors.values_list('sponsor__email',
                                                    flat=True)
    for email in relevant_emails:
        ctx = {
            'runner': runner.username,
            'kilometers': run.distance,
            'title': _("Masanga Runners run-update"),
        }
        html_msg = loader.get_template('runs/email/run_update.html')\
            .render(Context(ctx))
        subject = _('Masanga Runners run-update')
        send_mail(subject,
                  "",
                  settings.DEFAULT_FROM_EMAIL,
                  [email, ],
                  fail_silently=False,
                  html_message=html_msg)
