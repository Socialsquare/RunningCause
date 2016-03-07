# -*- coding: utf-8 -*-

import datetime
import calendar

from django.core.management.base import BaseCommand

from runs.tasks import send_input_runs_reminder


class Command(BaseCommand):
    help = 'Send input your runs reminder'

    def add_arguments(self, parser):
        parser.add_argument('--forced',
                            action='store_true',
                            dest='forced',
                            default=False,
                            help='Force the sending of reminders')

    def handle(self, *args, **options):
        todays = datetime.date.today()
        #last_day = calendar.monthrange(todays.year, todays.month)[1]
        if todays.day == 26 or options.get('forced'):
            emails_sent = send_input_runs_reminder()
            print 'A total of %d reminder emails have been sent' % emails_sent
        else:
            print('This command runs only on the 26th day of the month '
                  'use the --forced to do it anyway.')
