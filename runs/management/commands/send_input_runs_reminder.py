# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from runs.tasks import send_input_runs_reminder


class Command(BaseCommand):
    help = 'Send input your runs reminder'

    def handle(self, *args, **options):
        send_input_runs_reminder()
        print 'Reminder emails have been sent'
