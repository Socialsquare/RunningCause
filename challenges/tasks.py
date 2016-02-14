# coding: utf8
from __future__ import absolute_import

import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template import loader, Context

from common.helpers import send_email

from .models import Challenge


log = get_task_logger(__name__)


def send_challenge_reminder(user_id):
    user = get_user_model().objects.get(id=user_id)
    today = datetime.date.today()
    filters = {
        'status': Challenge.ACTIVE,
        'end_date': today
    }
    ending_challenges = user.challenges_recieved.filter(**filters)

    email_subject = _('Challenge ends today!')
    email_context = {
        'ending_challenges': ending_challenges,
        'BASE_URL': settings.BASE_URL,
    }

    send_email([user.email],
               email_subject,
               'challenges/emails/challenges_reminder.html',
               email_context)


@shared_task(ignore_result=True)
def send_challenge_reminders():
    # Fetch runners that has challenges ending today.
    today = datetime.date.today()
    filters = {
        'is_active': True,
        'challenges_recieved__end_date': today
    }
    relevant_runners = get_user_model().objects.filter(**filters)
    for runner in relevant_runners:
        send_challenge_reminder(runner.id)
