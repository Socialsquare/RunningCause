# coding: utf8
from __future__ import absolute_import

import datetime
from datetime import time

import requests
from celery import shared_task
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, Context


@shared_task(name='add')
def add(x, y):
    """
    Test task `add`
    """
    return x + y


@shared_task(name='pull_user_runs_from_runkeeper', ignore_result=True)
def pull_user_runs_from_runkeeper(user_id=None):
    assert user_id
    from runs.models import Run
    user = get_user_model().objects.get(id=user_id)
    # Request the workout data for the user using our new, shiny access
    # token.
    headers= {'Authorization': 'Bearer %s' % user.access_token}
    r = requests.get('https://api.runkeeper.com/fitnessActivities',
                     headers=headers)

    # Convert the workout data from JSON to make it easier to work with.
    data = r.json()

    # Get all runs that are associated with the user, and that came from runkeeper.
    # Compile all the of the source ids for them (the ids that were given to them
    # by their source, in this case runkeeper). This is important so that we make
    # sure that we don't register the same run multiple times.
    runkeeper_runs = user.runs.filter(source="runkeeper")
    registered_ids = [run.source_id for run in runkeeper_runs]

    # For each workout in the returned data...
    for item in data['items']:

        # If the workout hasn't already been registered with us...
        if item['uri'] not in registered_ids:

            # This coming block of code looks terrible. Unfortunately, there's not much
            # we can do about that.

            # Check to see how long the start_time item is. Here's why: the runkeeper API
            # does make some effort to make sure that their dates are easily machine readable
            # (the months are 3 letter abreviations, etc.). Unfortunately, they don't pad the
            # day of the month to make sure it's 2 digits. So, they'll return 11, 21, 31, but
            # will also return 1 instead of 01. This is the only thing that changes length in
            # in the whole date format, so you're gonna wann look out for that. If the day of
            # the month has 1 digit, then the whole string has length 24. Otherwise, it has
            # length 25.
            if len(item['start_time']) == 24:

                # Here, we're making a datetime object from our string using the strptime function.
                # You may notice the "[5:15]" section of this line. This is because the date contains
                # a lot of information that's not useful to us, so we're just stripping this out.
                # We're making a datetime assuming the format day of the month, month abbreviation, and
                # 4 digit year.
                date = time.strptime(item['start_time'][5:15], "%d %b %Y")

            # This means we've gotten a 2 digit day of the month. Proceed as above, just stripping
            # differently.
            else:

                # Here, we're making a datetime object from our string using the strptime function.
                # You may notice the "[5:16]" section of this line. This is because the date contains
                # a lot of information that's not useful to us, so we're just stripping this out.
                # We're making a datetime assuming the format day of the month, month abbreviation, and
                # 4 digit year.
                date = time.strptime(item['start_time'][5:16], "%d %b %Y")

            # This line is terrible. However, it works, and it works well. This creates a new date object
            # from the datetime object we just created.
            date = datetime.datetime(*date[:6]).date()

            # Create a new run object from the information we've assembled about the workout, and save it.
            # The distance value is divided by 1000 because runkeeper gives the distance in metres,
            # while our website stores them as kilometers.
            new_run = Run(runner=user,
                          distance=item['total_distance'] / 1000,
                          start_date=date,
                          end_date=date,
                          source="runkeeper",
                          source_id=item['uri'])
            new_run.save()


@shared_task(name='notify_sponsors_about_run', ignore_result=True)
def notify_sponsors_about_run(run_id=None):
    """
    Notify sponsors about the run
    """
    from runs.models import Run
    assert run_id
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
