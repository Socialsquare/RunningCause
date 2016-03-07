# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from challenges.tasks import send_challenge_reminders

from django.utils import translation
from django.conf import settings


class Command(BaseCommand):
    help = 'Updates all people on the status of their challenges.'

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        send_challenge_reminders()
