# coding: utf8
from __future__ import absolute_import

import logging
from datetime import timedelta

from dateutil.parser import parse
import requests

from django.contrib.auth import get_user_model

from .models import Run, RunkeeperToken

log = logging.getLogger(__name__)


RUNKEEPER_BASE_URL = 'https://api.runkeeper.com'


def rk_items_to_runs(user, items):
    already_registered_sids = user.runs.exclude(source_id='')\
        .filter(source="runkeeper")\
        .values_list('source_id', flat=True)
    buff = []
    for item in items:
        if item['uri'] in already_registered_sids:
            continue
        if item['type'].lower() != 'running':
            continue

        date = parse(item['start_time'])
        # if not item['utc_offset']:
        #    date = date.replace(tzinfo=timezone.UTC)
        duration = timedelta(seconds=item['duration'])
        buff.append(Run(runner=user,
                        distance=item['total_distance'] / 1000.0,
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
    token = RunkeeperToken.objects.get(runner=user).access_token

    # TODO: create RunkeeperClient class or use some lib github
    # FIXME: get all items from paginated lists!
    headers = {
        'Authorization': 'Bearer %s' % (token, ),
        'Accept': '',
    }
    url = RUNKEEPER_BASE_URL + '/user'
    headers['Accept'] = 'application/vnd.com.runkeeper.User+json'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    user_data = resp.json()

    url = RUNKEEPER_BASE_URL + user_data['fitness_activities']
    headers['Accept'] = 'application/vnd.com.runkeeper.FitnessActivityFeed+json'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    log.debug("Received %d items", len(data['items']))
    rk_items_to_runs(user, data['items'])


def pull_all_users_runs_from_runkeeper():
    usersids_with_tokens = RunkeeperToken.objects\
        .values_list('runner_id', flat=True)
    for user_id in usersids_with_tokens:
        create_runs_from_runkeeper(user_id=user_id)
