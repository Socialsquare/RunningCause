
from django.core.management.base import BaseCommand

from payments.tasks import charge_users


class Command(BaseCommand):
    help = 'Charges all customers who have registered with stripe'

    def handle(self, *args, **options):
        charge_users()
