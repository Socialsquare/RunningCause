from django.db import models
import django.contrib.auth as auth
from django.core.urlresolvers import reverse

from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import sys

# Add admin Url to every content object
def get_admin_url(self):
    return reverse('admin:%s_%s_change' % (self._meta.app_label,  self._meta.module_name),  args=[self.pk])

models.Model.get_admin_url = get_admin_url

class User(auth.models.AbstractUser):
    USERNAME_FIELD = 'username'
    is_public = models.BooleanField('Info public?', default=False)
    access_token = models.CharField('Access token', max_length=200, default="", blank=True)

    @property
    def is_runner(self):
        any_runs_or_sponsorships = max(len(self.runs.all()), len(self.sponsorships_recieved.all()))
        return any_runs_or_sponsorships > 0

    @property
    def is_sponsor(self):
        num_sponsorships = len(self.sponsorships_given.all())
        return num_sponsorships > 0

class Sponsorship(models.Model):
    runner = models.ForeignKey(User, related_name='sponsorships_recieved')
    sponsor = models.ForeignKey(User, related_name='sponsorships_given', null=True)
    rate = models.FloatField('Rate', default=0, null=True)
    start_date = models.DateField('Start Date', default = date.today(), null=True)
    end_date = models.DateField('End Date', default=date.today()+relativedelta(months=1), null=True)
    max_amount = models.IntegerField('Max Amount', default=sys.maxint, null=True)
    amount_paid = models.IntegerField('Amount Paid', default=0)

    @property
    def is_active(self):
        if date.today() < self.end_date and date.today() >= self.start_date and self.total_amount < self.max_amount:
            return True
        return False

    @property
    def total_amount(self):
        amount = 0
        for run in self.runner.runs.all():
            if run.start_date >= self.start_date and run.end_date < self.end_date:
                amount = amount + (self.rate * run.distance)
        amount = min(amount, self.max_amount)
        return amount

    @property
    def left_to_pay(self):
        return self.total_amount - self.amount_paid

    def save(self, *args, **kwargs):
        if self.sponsor != None:
            if self.rate is None or self.start_date is None or self.end_date is None or self.max_amount is None:
                print "SOMETHING HAS GONE VERY WRONG PANIC SPONSORSHIP FIELDS WRONG"
        super(Sponsorship, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.sponsor

class Run(models.Model):
    runner = models.ForeignKey(User, related_name='runs')
    distance = models.FloatField('Distance', default=1)
    start_date = models.DateField('Date', default=date.today())
    end_date = models.DateField('End Date', default=date.today())
    source = models.CharField('Source', default="", max_length=200)
    source_id = models.CharField('Source ID', default="", max_length=200)

    def __unicode__(self):
        return'%s' % self.distance
