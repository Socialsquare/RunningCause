import datetime
from django.core.management.base import BaseCommand

from payments.tasks import charge_users


class Command(BaseCommand):
    help = 'Charges all customers who have registered with stripe'

    def handle(self, *args, **options):
        # FIXME: hack because celery on heroku is expensive..
        today = datetime.date.today()
        if today.month in (1, 4, 7, 10) and today.day == 1:
            charge_users()
        else:
            print "Skipping... We only charge users the first day of a quarter!"
