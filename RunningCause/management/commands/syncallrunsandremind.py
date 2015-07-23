# -*- coding: utf-8 -*-

import sys
import datetime

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader, Context
from django.contrib.auth import get_user_model

from runs.runkeeper import pull_all_users_runs_from_runkeeper


class Command(BaseCommand):
    help = 'Updates the runs of all users that have registered with runkeeper'

    def handle(self, *args, **options):
        if datetime.datetime.today().day != 1:
            print "this runs only first day of the month"
            sys.exit(1)

        pull_all_users_runs_from_runkeeper()

        self.stdout.write('Successfully updated runs')
        subscribed_users = get_user_model.objects.filter(subscribed=True)
        all_addresses = [juser.email for juser in subscribed_users
                         if (juser.is_runner and juser.email)]

        # TODO: fix the rest of this...

        message = 'Hej Masanga Runner\n\nHar du været ude og løbe, og har du ikke registreret dette manuelt på Masanga Runners eller via RunKeeper, så er det måske ved at være tid.\n\nwww.runners.masanga.dk\n\nDu bestemmer selv, hvor ofte du vil registrere dine kilometer, og om du vil koble dig op med RunKeeper, men vi anbefaler at du registrerer dine kilometer mindst en gang om måneden.\n\nTak fordi du løber for Masanga! Rigtig god løbelyst.'

        for address in all_addresses:
            if address:
                send_mail('Reminder', 
                            message,
                            'postmaster@appa4d174eb9b61497e90a286ddbbc6ef57.mailgun.org', 
                            [address], 
                            fail_silently=False,
                            html_message=loader.get_template('Running/email.html').render(Context({'message': message, 
                                                                                                    'request': None, 
                                                                                                    'domain': settings.BASE_URL,
                                                                                                    'title': "Masanga Runners Reminder"})))

        self.stdout.write('Sent reminder mail')