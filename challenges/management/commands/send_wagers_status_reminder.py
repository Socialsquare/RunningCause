# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from challenges.tasks import send_challenge_reminders


class Command(BaseCommand):
    help = 'Updates all people on the status of their challenges.'

    def handle(self, *args, **options):
        send_challenge_reminders()
