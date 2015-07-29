# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from wagers.tasks import send_wager_reminders


class Command(BaseCommand):
    help = 'Updates all people on the status of their wagers.'

    def handle(self, *args, **options):
        send_wager_reminders()
