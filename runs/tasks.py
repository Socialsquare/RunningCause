# coding: utf8
from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger

from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import loader, Context


from common.helpers import send_email

from .runkeeper import create_runs_from_runkeeper


log = get_task_logger(__name__)


@shared_task(ignore_result=True)
def pull_user_runs_from_runkeeper(user_id=None):
    create_runs_from_runkeeper(user_id=user_id)


@shared_task(ignore_result=True)
def notify_sponsors_about_run(run_id=None):
    """
    Notify sponsors about the run
    """
    from runs.models import Run
    run = Run.objects.select_related('runner').get(id=run_id)
    runner = run.runner
    relevant_sponsors = runner.sponsorships_recieved\
        .filter(end_date__gte=run.start_date, start_date__lte=run.start_date)\
        .exclude(sponsor__isnull=True)\
        .distinct('sponsor')

    relevant_emails = relevant_sponsors.values_list('sponsor__email',
                                                    flat=True)
    for email in relevant_emails:
        ctx = {
            'runner_username': runner.username,
            'kilometers': run.distance,
            'title': _("Masanga Runners run-update"),
            'BASE_URL': settings.BASE_URL,
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


@shared_task(ignore_result=True)
def send_input_runs_reminder():
    # Find all subscribed users that has entered runs
    subscribed_users = get_user_model().objects.filter(subscribed=True)

    all_addresses = [user.email
                     for user in subscribed_users
                     if user.is_runner and user.email]

    email_context = {
        'enter_run_link': settings.BASE_URL+reverse('runs:input_run'),
        'runkeeper_link': settings.BASE_URL+reverse('runs:register_runkeeper')
    }
    emails_sent = 0
    for email in all_addresses:
        emails_sent += send_email(email,
                                  _('It is time to register runs'),
                                  'runs/email/input_runs_reminder.html',
                                  email_context)
    return emails_sent
