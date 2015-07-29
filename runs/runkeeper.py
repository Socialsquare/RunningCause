# coding: utf8
from __future__ import absolute_import

import logging
from datetime import timedelta

from dateutil.parser import parse
import requests

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Run

log = logging.getLogger(__name__)


# TODO extract uri from user resource
RUNKEEPER_FITNESS_ACTIVITIES = 'https://api.runkeeper.com/fitnessActivities'


def rk_items_to_runs(user, items):
    already_registered_sids = user.runs.exclude(source_id='')\
        .filter(source="runkeeper")\
        .values_list('source_id', flat=True)
    buff = []
    for item in items:
        if item['uri'] in already_registered_sids:
            continue
        if item['type'].lower() != ' running':
            continue

        date = parse(item['start_time'])
        # if not item['utc_offset']:
        #    date = date.replace(tzinfo=timezone.UTC)
        duration = timedelta(seconds=item['duration'])
        buff.append(Run(runner=user,
                        distance=item['total_distance'] / 1000,
                        start_date=date,
                        end_date=date,
                        source="runkeeper",
                        source_id=item['uri'],
                        recorded_time=duration))
        if len(buff) >= 1000:
            Run.objects.bulk_create(buff)
            buff = []
    if buff:
        Run.objects.bulk_create(buff)


def create_runs_from_runkeeper(user_id=None):
    user = get_user_model().objects.get(id=user_id)
    headers = {
        'Authorization': 'Bearer %s' % user.access_token,
        'Accept': 'application/vnd.com.runkeeper.FitnessActivitySummary+json'
    }
    r = requests.get(RUNKEEPER_FITNESS_ACTIVITIES, headers=headers)
    data = r.json()
    log.debug("Received %d items", len(data['items']))
    rk_items_to_runs(user, data['items'])


def pull_all_users_runs_from_runkeeper():
    usersids_with_tokens = get_user_model().objects\
        .exclude(access_token="")\
        .values_list('id', flat=True)
    for user_id in usersids_with_tokens:
        create_runs_from_runkeeper(user_id=user_id)
