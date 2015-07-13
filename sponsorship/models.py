import uuid
from decimal import Decimal
from datetime import date

from django.db import models
from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta


class Sponsorship(models.Model):
    """
    The model for every sponsorship.
    """

    #    The user that is recieving this sponsorship.
    runner = models.ForeignKey(get_user_model(),
                               related_name='sponsorships_recieved')

    #   The user that is giving this sponsorship.
    sponsor = models.ForeignKey(get_user_model(),
                                related_name='sponsorships_given', null=True)

    #   The rate, in kroner per kilometer, of the sponsorship. 
    rate = models.DecimalField('Rate', default=0, max_digits=10,
                               decimal_places=2, null=True)

    #   The start date. No runs before this date are added to the sponsorship.
    start_date = models.DateField('Start Date', auto_now_add=True,
                                  null=True, db_index=True)

    # The end date. No runs after or on this date are added to the sponsorship.
    # (end date is exclusive!)
    end_date = models.DateField('End Date',
                                default=lambda: date.today() + \
                                                relativedelta(months=1),
                                null=True, db_index=True)

    #   The maximum possible amount of money for the sponsorship.
    # No more runs are counted once this
    #   amount is reached.
    max_amount = models.DecimalField('Max Amount', default=10000,
                                     max_digits=10, decimal_places=2,
                                     null=True)

    #   The amount of money on the sponsorship that has already been paid.
    # Used for manually keeping
    #   track of how much has been paid and how much is left to pay.
    amount_paid = models.DecimalField('Amount Paid', default=0,
                                      max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Running_sponsorship'

    #   This determines whether or not the sponsorship is currently active.
    # Sponsorships are considered
    #   active if the current date is between start_date and end_date,
    # and the total amount for the
    #   sponsorship is currently less that max_amount.
    @property
    def is_active(self):
        if date.today() < self.end_date and \
                date.today() > self.start_date and \
                self.total_amount < self.max_amount:
            return True
        return False

    #   Calculates how much money has been raised under the current
    # sponsorship. Finds all relevant runs,
    #   and returns either the sum of all relevant runs, or max_amount,
    # whichever is less.
    @property
    def total_amount(self):
        distances = self.runner.runs.filter(start_date__gte=self.start_date,
                                            end_date__lte=self.end_date)\
                                            .values_list('distance', flat=True)
        amount = sum([self.rate * Decimal(distance) for distance in distances])
        return min(amount, self.max_amount)

    #   Returns the amount of money left to pay, by subtracting amount_paid
    # from total_amount.
    @property
    def left_to_pay(self):
        return self.total_amount - self.amount_paid

    def __unicode__(self):
        return '%s -> %s' % (self.sponsor, self.runner)


class SponsorRequest(models.Model):
    runner = models.ForeignKey(get_user_model())
    sponsor = models.ForeignKey(get_user_model())
    created_dt = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4,
                             unique=True, db_index=True, null=False,
                             editable=False, primary_key=False)
    sponsorship = models.ForeignKey(Sponsorship, null=True)
    proposed_sponsorship = models.TextField()

    def __unicode__(self):
        return '%s (->) %s' % (self.sponsor, self.runner)
