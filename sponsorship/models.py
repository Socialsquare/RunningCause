import uuid
from decimal import Decimal
from datetime import date

from django.db import models
from django.db.models import Sum, Q
from django.conf import settings
from dateutil.relativedelta import relativedelta


def get_default_end_date():
    return date.today() + relativedelta(months=1)


class Sponsorship(models.Model):
    """
    The model for every sponsorship.
    """

    # The user that is receiving the sponsorship.
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='sponsorships_recieved',
                               null=False)

    # The user that is giving the sponsorship.
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='sponsorships_given',
                                null=False)

    # The rate, in currency, per kilometer, of the sponsorship.
    rate = models.DecimalField('Rate', default=0, max_digits=10,
                               decimal_places=2, null=True)

    # The start date. No runs before this date are added to the sponsorship.
    # (start date is inclusive)
    start_date = models.DateField('Start Date', null=True, db_index=True)

    # The end date. No runs after or on this date are added to the sponsorship.
    # (end date is exclusive!)
    end_date = models.DateField('End Date',
                                default=get_default_end_date,
                                null=True, db_index=True, blank=True)

    # The maximum possible amount of money for the sponsorship.
    # No more runs are counted once this
    # amount is reached.
    max_amount = models.DecimalField('Max Amount', default=10000,
                                     max_digits=10, decimal_places=2,
                                     null=True)

    # The amount of money on the sponsorship that has already been paid.
    # Used for manually keeping
    # track of how much has been paid and how much is left to pay.
    amount_paid = models.DecimalField('Amount Paid', default=0,
                                      max_digits=10, decimal_places=2)

    @property
    def is_active(self):
        """
        This determines whether or not the sponsorship is currently active.
        Sponsorships are considered
        active if the current date is between start_date
        and end_date (exclusive), and the total amount for the
        sponsorship is currently less or equal to max_amount.
        """
        today = date.today()
        has_started = today >= self.start_date
        has_not_ended = not self.end_date or today < self.end_date
        amount_left = not self.max_amount or \
            self.total_amount <= self.max_amount

        return has_started and has_not_ended and amount_left

    @property
    def total_amount(self):
        """
        Calculates how much money has been raised under the current
        sponsorship. Finds all relevant runs,
        and returns either the sum of all relevant runs, or max_amount,
        whichever is less.
        """
        filters = {
            'start_date__gte': self.start_date
        }
        if self.end_date:
            filters['end_date__lte'] = self.end_date
        distance = self.runner.runs.filter(**filters) \
            .aggregate(a_sum=Sum('distance'))['a_sum'] or 0
        amount = self.rate * Decimal(distance)
        if self.max_amount:
            return min(amount, self.max_amount)
        else:
            return amount

    @property
    def left_to_pay(self):
        """
        Returns the amount of money left to pay.
        """
        return self.total_amount - self.amount_paid

    def __unicode__(self):
        return '%s -> %s' % (self.sponsor, self.runner)


class SponsorRequest(models.Model):
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='sponsorships_requested')
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='sponsorships_requests')
    created_dt = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4,
                             unique=True, db_index=True, null=False,
                             editable=False, primary_key=False)
    sponsorship = models.ForeignKey(Sponsorship, null=True)
    proposed_sponsorship = models.TextField()  # json field

    def __unicode__(self):
        return '%s (->) %s' % (self.sponsor, self.runner)
