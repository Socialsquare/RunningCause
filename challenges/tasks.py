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


log = get_task_logger(__name__)


def send_challenge_reminder(user_id=None):
    from .models import Challenge
    user = get_user_model().objects.get(id=user_id)
    todays = datetime.date.today()
    remind_delta = todays + Challenge.get_remind_date_delta()
    received_ending_soon_challenges = user.challenges_recieved\
        .filter(status=Challenge.ACTIVE, end_date=remind_delta)

    decision_delta = todays - Challenge.get_decision_date_delta()
    given_completed_challenges = user.challenges_given\
        .filter(status=Challenge.COMPLETED, end_date=decision_delta)

    if not received_ending_soon_challenges and not given_completed_challenges:
        log.debug("user %s has no completed or ending soon challenges", user.id)
        return

    subject = _('Masanga Runners challenge reminder')
    tmpl_name = 'challenges/emails/challenges_reminder.html'
    tmpl = loader.get_template(tmpl_name)
    ctx = Context({
        'received_ending_soon_challenges': received_ending_soon_challenges,
        'given_completed_challenges': given_completed_challenges,
        'BASE_URL': settings.BASE_URL,
    })
    html_msg = tmpl.render(ctx)
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email],
              fail_silently=False, html_message=html_msg)


@shared_task(ignore_result=True)
def send_challenge_reminders():
    active_users_ids = get_user_model().objects.filter(is_active=True)\
        .values_list('id', flat=True)
    for user_id in active_users_ids:
        send_challenge_reminder(user_id=user_id)
