import sys
import datetime
from decimal import Decimal, ROUND_UP

import stripe
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model

from sponsorship.models import Sponsorship


stripe.api_key = settings.STRIPE_SECRET_KEY


def format_amount_to_pay(amount_to_pay):
    """

    >>> format_amount_to_pay(12.345)
    1235
    """
    amount_to_pay = Decimal(amount_to_pay)\
        .quantize(Decimal("0.00"), rounding=ROUND_UP)
    amount_to_pay = "%.2f" % amount_to_pay
    amount_to_pay = ''.join(amount_to_pay.split('.'))
    amount_to_pay = int(amount_to_pay)
    return amount_to_pay


@transaction.atomic()
def charge_user(user_id=None):
    user = get_user_model().objects.get(id=user_id)
    amount_to_pay = 0
    sponsorships = user.sponsorships_given.all()
    spltp = [(sp.id, sp.amount_paid, sp.left_to_pay)
             for sp in sponsorships
             if sp.left_to_pay > 0]
    amount_to_pay += sum([spl[2] for spl in spltp])
    unpaid_wagers = user.wagers_given.filter(paid=False,
                                             fulfilled=True)
    amount_to_pay += sum([wager.amount for wager
                          in unpaid_wagers])
    amount = format_amount_to_pay(amount_to_pay)
    print "%s\t%f (%s)..." % (user.username, amount_to_pay, amount)
    if amount_to_pay != 0:
        stripe_status = stripe.Charge.create(
            amount=amount,
            currency="dkk",
            customer=user.stripe_customer_id
        ).get("status")
        if stripe_status == "succeeded":
            for sp_id, amount_paid, left_to_pay in spltp:
                Sponsorship.objects.filter(id=sp_id)\
                    .update(amount_paid=amount_paid + left_to_pay)
            unpaid_wagers.update(paid=True)

            print "{0} charged {1}".format(user.username,
                                           amount)
        else:
            emsg = "ERROR: Stripe returned {0}".format(stripe_status)
            raise Exception(emsg)


class Command(BaseCommand):
    help = 'Charges all customers who have registered with stripe'

    def handle(self, *args, **options):
        if not datetime.datetime.today().day == 1:
            print "this runs only first day of the month"
            sys.exit(0)

        users_ids = get_user_model().objects\
            .exclude(stripe_customer_id=None).values_list('id', flat=True)
        for user_id in users_ids:
            try:
                charge_user(user_id=user_id)
            except Exception as exc:
                print "ERROR: charging user {} failed".fomat(user_id)
                print "{}".fomat(exc)

