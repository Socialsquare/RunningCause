
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from runs.runkeeper import pull_all_users_runs_from_runkeeper


class Command(BaseCommand):
    help = 'Updates runs of all users that have registered with runkeeper'

    def handle(self, *args, **options):
        pull_all_users_runs_from_runkeeper()
        print 'Successfully updated runs for all users'
