# coding: utf8
from __future__ import absolute_import

import stripe
from celery import shared_task
from celery.utils.log import get_task_logger

from django.db import transaction
from django.conf import settings

from .utils import format_amount_to_pay


log = get_task_logger(__name__)


@transaction.atomic()
def charge_user(user_id=None):
    from .models import PaymentLog
    from sponsorship.models import Sponsorship
    from wagers.models import Wager
    from django.contrib.auth import get_user_model

    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = get_user_model().objects.get(id=user_id)
    amount_to_pay = 0
    sponsorships = user.sponsorships_given.all()
    spltp = [(sp.id, sp.amount_paid, sp.left_to_pay)
             for sp in sponsorships
             if sp.left_to_pay > 0]
    amount_to_pay += sum([spl[2] for spl in spltp])
    unpaid_wagers = user.wagers_given.filter(status=Wager.CONFIRMED)
    amount_to_pay += sum([wager.amount for wager
                          in unpaid_wagers])
    if amount_to_pay == 0:
        return

    amount = format_amount_to_pay(amount_to_pay)
    log.info("%s\t%f (%s)...", user.username, amount_to_pay, amount)

    stripe_status = stripe.Charge.create(
        amount=amount,
        currency="dkk",
        customer=user.stripe_customer_id,
        receipt_email=user.email
    ).get("status")
    if stripe_status == "succeeded":
        PaymentLog.objects.create(user=user, amount=amount_to_pay)
        for sp_id, amount_paid, left_to_pay in spltp:
            Sponsorship.objects.filter(id=sp_id)\
                .update(amount_paid=amount_paid + left_to_pay)
        unpaid_wagers.update(status=Wager.PAID)

        log.info("{0} charged {1}".format(user.username,
                                          amount))
    else:
        emsg = "ERROR: Stripe returned {0}".format(stripe_status)
        raise Exception(emsg)


@shared_task(ignore_result=True)
def charge_users():
    from django.contrib.auth import get_user_model
    users_ids = get_user_model().objects\
        .exclude(stripe_customer_id=None).values_list('id', flat=True)
    for user_id in users_ids:
        try:
            charge_user(user_id=user_id)
        except Exception as exc:
            log.error("charging user %s failed", user_id, exc_info=1)
