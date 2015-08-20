# -*- coding: utf-8 -*-

import datetime
import calendar

from django.core.management.base import BaseCommand

from runs.tasks import send_input_runs_reminder


class Command(BaseCommand):
    help = 'Send input your runs reminder'

    def handle(self, *args, **options):
        todays = datetime.date.today()
        last_day = calendar.monthrange(todays.year, todays.month)[1]
        if last_day == todays.day:
            send_input_runs_reminder()
            print 'Reminder emails have been sent'
        else:
            print 'This command runs only on the last day of the month'
