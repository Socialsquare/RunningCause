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


def send_wager_reminder(user_id=None):
    from .models import Wager
    user = get_user_model().objects.get(id=user_id)
    todays = datetime.date.today()
    remind_delta = todays + Wager.get_remind_date_delta()
    received_ending_soon_wagers = user.wagers_recieved\
        .filter(status=Wager.NEW, end_date=remind_delta)

    decision_delta = todays - Wager.get_decision_date_delta()
    given_completed_wagers = user.wagers_given\
        .filter(status=Wager.COMPLETED, end_date=decision_delta)

    if not received_ending_soon_wagers and not given_completed_wagers:
        log.debug("user %s has no completed or ending soon wagers", user.id)
        return

    subject = _('Masanga Runners challenge reminder')
    tmpl_name = 'wagers/emails/wagers_reminder.html'
    tmpl = loader.get_template(tmpl_name)
    ctx = Context({
        'received_ending_soon_wagers': received_ending_soon_wagers,
        'given_completed_wagers': given_completed_wagers,
        'BASE_URL': settings.BASE_URL,
    })
    html_msg = tmpl.render(ctx)
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email],
              fail_silently=False, html_message=html_msg)


@shared_task(ignore_result=True)
def send_wager_reminders():
    active_users_ids = get_user_model().objects.filter(is_active=True)\
        .values_list('id', flat=True)
    for user_id in active_users_ids:
        send_wager_reminder(user_id=user_id)
