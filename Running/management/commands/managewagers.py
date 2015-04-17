# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand, CommandError
from Running.models import User, Run
import requests
import datetime
import json
import time
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template import RequestContext, loader, Context, Template


class Command(BaseCommand):
    help = 'Updates all people on the status of their wagers.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        all_users = User.objects.all()
        for user in all_users:
            for wager in user.wagers_recieved.exclude(sponsor=None):
                if wager.remind_date == datetime.date.today():
                    update_url = reverse('update_wager', kwargs={'wager_id': wager.id})
                    message_text = "Dit væddemål med {0} slutter i dag. Klik her for at sende en update om, hvordan det er gået: {1}\n\nUanset om du reagerer, vil {0} i morgen blive bedt om at beslutte, om du vandt væddemålet.".format(wager.sponsor,
                                                                                                                                                                                                                        settings.BASE_DOMAIN[:-1] + update_url)
                    send_mail('Masanga Runners update på væddemål ', 
                                message_text, 
                                settings.DEFAULT_FROM_EMAIL,
                                [wager.runner.email], 
                                fail_silently=False,
                                html_message = loader.get_template('Running/email.html').render(Context({'message': message_text, 'domain': settings.BASE_DOMAIN})))
            for wager in user.wagers_given.all():
                if wager.decision_date() == datetime.date.today():
                    confirm_url = reverse('confirm_wager', kwargs={'wager_id': wager.id})
                    decline_url = reverse('decline_wager', kwargs={'wager_id': wager.id})

                    if wager.update_text:
                        message_text = "Your wager with {0} has ended. {0} said: {1}. Just a reminder, the wager said {2}. Click here to confirm that the wager was successfully completed: {3}, or here to say that the wager was failed: {4}".format(wager.runner, 
                                                                                                                                                                                                                        wager.update_text,
                                                                                                                                                                                                                        wager.wager_text,
                                                                                                                                                                                                                        settings.BASE_DOMAIN[:-1] + confirm_url,
                                                                                                                                                                                                                        settings.BASE_DOMAIN[:-1] + decline_url)
                    else:
                        message_text = "Your wager with {0} has ended. Just a reminder, the wager said {1}. Click here to confirm that the wager was successfully completed: {2}, or here to say that the wager was failed: {3}".format(wager.runner, 
                                                                                                                                                                                                                        wager.wager_text,
                                                                                                                                                                                                                        settings.BASE_DOMAIN[:-1] + confirm_url,
                                                                                                                                                                                                                        settings.BASE_DOMAIN[:-1] + decline_url)
                    send_mail('Dit væddemål på Masanga Runners er ovre', 
                                message_text, 
                                settings.DEFAULT_FROM_EMAIL,
                                [wager.sponsor.email], 
                                fail_silently=False,
                                html_message = loader.get_template('Running/email.html').render(Context({'message': message_text, 'domain': settings.BASE_DOMAIN})))