from django.db import models
import django.contrib.auth as auth
from django.core.urlresolvers import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import sys

#   Add admin Url to every content object
def get_admin_url(self):
    return reverse('admin:%s_%s_change' % (self._meta.app_label,  self._meta.model_name),  args=[self.pk])

models.Model.get_admin_url = get_admin_url

#   The model for every user. Extends auth.models.AbstractUser, and adds 2 fields and 2 properties.
class User(auth.models.AbstractUser):
    #   Since this is a custom class, we have to tell Django which field to treat as our username.
    USERNAME_FIELD = 'username'

    #   This variable determines whether or not we display the user's profile and sponsorships publicly.
    is_public = models.BooleanField('Info public?', default=False)

    #   This variable is an access token to be used with RunKeeper, if the user has connected with it yet.
    access_token = models.CharField('Access token', max_length=200, default="", blank=True)

    newsletter = models.BooleanField('Newsletter?', default=False)

    #   This determines whether or not our user is a "runner". This is only to affect some UI on their profile.
    @property
    def is_runner(self):
        any_runs_or_sponsorships = max(len(self.runs.all()), len(self.sponsorships_recieved.all()))
        return any_runs_or_sponsorships > 0

    #   This determines whether or not our user is a "sponsor". This is only to affect some UI on their profile.
    @property
    def is_sponsor(self):
        num_sponsorships = len(self.sponsorships_given.all())
        return num_sponsorships > 0

    #   This figures out how much the user has raised for Masanga.
    @property
    def amount_earned(self):
        total_amount = 0
        for sponsorship in self.sponsorships_recieved.all():
            if sponsorship.sponsor != None:
                total_amount = total_amount + sponsorship.total_amount
        return total_amount

    #   This figures out how much the user has donated to Masanga through sponsorships.
    @property
    def amount_donated(self):
        total_amount = 0
        for sponsorship in self.sponsorships_given.all():
            total_amount = total_amount + sponsorship.total_amount
        return total_amount


#   The model for every sponsorship.
class Sponsorship(models.Model):
    #    The user that is recieving this sponsorship.
    runner = models.ForeignKey(User, related_name='sponsorships_recieved')
    
    #   The user that is giving this sponsorship.
    sponsor = models.ForeignKey(User, related_name='sponsorships_given', null=True)

    #   The rate, in kroner per kilometer, of the sponsorship. 
    rate = models.FloatField('Rate', default=0, null=True)

    #   The start date. No runs before this date are added to the sponsorship.
    start_date = models.DateField('Start Date', default = date.today(), null=True)

    #   The end date. No runs after this date are added to the sponsorship.
    end_date = models.DateField('End Date', default=date.today()+relativedelta(months=1), null=True)

    #   The maximum possible amount of money for the sponsorship. No more runs are counted once this
    #   amount is reached.
    max_amount = models.FloatField('Max Amount', default=sys.maxint, null=True)

    #   The amount of money on the sponsorship that has already been paid. Used for manually keeping
    #   track of how much has been paid and how much is left to pay.
    amount_paid = models.IntegerField('Amount Paid', default=0)

    #   This determines whether or not the sponsorship is currently active. Sponsorships are considered
    #   active if the current date is between start_date and end_date, and the total amount for the
    #   sponsorship is currently less that max_amount.
    @property
    def is_active(self):
        if date.today() <= self.end_date and date.today() >= self.start_date and self.total_amount < self.max_amount:
            return True
        return False

    #   Calculates how much money has been raised under the current sponsorship. Finds all relevant runs,
    #   and returns either the sum of all relevant runs, or max_amount, whichever is less.
    @property
    def total_amount(self):
        amount = 0
        for run in self.runner.runs.all():
            if run.start_date >= self.start_date and run.end_date <= self.end_date:
                amount = amount + (self.rate * run.distance)
        amount = min(amount, self.max_amount)
        return amount

    #   Returns the amount of money left to pay, by subtracting amount_paid from total_amount.
    @property
    def left_to_pay(self):
        return self.total_amount - self.amount_paid

    #   Saves the sponsorship. modified to print an error to console if an invalid configuration of
    #   vairables is left null. Should eventually throw some sort of error.
    def save(self, *args, **kwargs):
        if self.sponsor != None:
            if self.rate is None or self.start_date is None or self.end_date is None or self.max_amount is None:
                print "SOMETHING HAS GONE VERY WRONG PANIC SPONSORSHIP FIELDS WRONG"
        super(Sponsorship, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.sponsor

#   The model for a specific run, or several runs over a period.
class Run(models.Model):
    #   The runner that ran the run.
    runner = models.ForeignKey(User, related_name='runs')

    #   The distance over the course of the run.
    distance = models.FloatField('Distance', default=1)

    #   Either the date of the run, or the start of the period over which the runs took place.
    start_date = models.DateField('Date', default=date.today())

    #   Either the date of the run, or the end of the period over which the runs took place.
    end_date = models.DateField('End Date', default=date.today())

    #   Where the runs were entered, if different from Masanga Runners. Used to keep track of
    #   which runs have already been entered.
    source = models.CharField('Source', default="", max_length=200)

    #   The id that was assigned to the run on whatever platform it came from, if different
    #   from Masanga Runners. Used to keep track of which runs have already been entered.
    source_id = models.CharField('Source ID', default="", max_length=200)

    def __unicode__(self):
        return'%s' % self.distance
