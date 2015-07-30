import datetime

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from runs.tasks import notify_sponsors_about_run
from runs.models import Run


class Command(BaseCommand):
    help = 'Notify sponsors about runs'

    def handle(self, *args, **options):
        # FIXME: hack because celery on heroku costs money
        # see scheduler frequency for 10 minutes
        scheduler_fr = datetime.timedelta(minutes=10)
        rangedt = timezone.now() - scheduler_fr
        new_runs = Run.objects.filter(Q(created_dt__gt=rangedt))
        for run in new_runs:
            notify_sponsors_about_run(run_id=run.id)
        print 'Successfully notified all sponsors'
