from django.core.management.base import BaseCommand, CommandError
from Running.models import User, Run
import requests
import datetime
import json
import time
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = 'Charges all customers who have registered with stripe'


    def handle(self, *args, **options):
        users_with_customers = User.objects.exclude(stripe_customer_id=None)
        amount_to_pay = 0
        for user in users_with_customers:
            for sponsorship in user.sponsorships_given.all():
                if sponsorship.left_to_pay > 0:
                    amount_to_pay = amount_to_pay + sponsorship.left_to_pay
                    print amount_to_pay
            for wager in user.wagers_given.filter(paid=False, fulfilled=True):
                amount_to_pay = amount_to_pay + wager.amount
                print amount_to_pay
            print amount_to_pay
            if amount_to_pay!=0:
                stripe_status = stripe.Charge.create(
                    amount=int(amount_to_pay*100),
                    currency="dkk",
                    customer=user.stripe_customer_id
                )["status"] 
                if stripe_status == "succeeded":
                    for sponsorship in user.sponsorships_given.all():
                        sponsorship.amount_paid = sponsorship.total_amount
                        sponsorship.save()
                    for wager in user.wagers_given.filter(paid=False, fulfilled=True):
                        wager.paid = True
                        wager.save()


                print "{0} charged {1}".format(user.username, amount_to_pay)
