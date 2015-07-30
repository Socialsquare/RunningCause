import datetime
from django.core.management.base import BaseCommand

from payments.tasks import charge_users


class Command(BaseCommand):
    help = 'Charges all customers who have registered with stripe'

    def handle(self, *args, **options):
        # FIXME: hack because celery on heroku is expensive...
        if datetime.date.today().month in (1, 4, 7, 10):
            charge_users()
        else:
            print "skipping call... we charge users quarterly only!"
