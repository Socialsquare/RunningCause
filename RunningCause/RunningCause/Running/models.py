from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
import calendar
import sys


class Sponsorship(models.Model):
    runner = models.ForeignKey(User)
    sponsor = models.CharField('Sponsor', max_length = 200)
    rate = models.FloatField('Rate')
    email = models.EmailField('Email', default="masanga@mailinator.com")
    start_date = models.DateField('Start Date', default = datetime.today(), editable=False)
    end_date = models.DateField('End Date', default=(datetime.today()+timedelta(weeks=4)))
    max_amount = models.IntegerField('Max Amount', default=sys.maxint)
    active = models.BooleanField('Active', default=True)

    @property
    def past_end_date(self):
        if datetime.today().date() >= self.end_date:
            active = False
            return True
        return False

    def pay(self):
        for payment in Payment.objects.filter(sponsorship__pk=self.id):
            payment.active = False
            payment.save()
        new_payment = Payment(sponsorship=self)

    def __unicode__(self):
        return '%s' % self.sponsor

class Run(models.Model):
    runner = models.ForeignKey(User)
    distance = models.FloatField('Distance', default=1)
    date = models.DateField('Date', default=datetime.today())

    def __unicode__(self):
        return'%s' % self.distance

class Payment(models.Model):
    sponsorship = models.ForeignKey(Sponsorship, related_name='payments')
    amount = models.IntegerField('Amount', default=0)
    active = models.BooleanField('Active', default=True)
    end_date = models.DateField('End date', default=datetime(datetime.today().year, datetime.today().month+1, 1), editable=False)

    @property
    def ended(self):
        return datetime.today() >= end_date

    def __unicode__(self):
        return '%s' % self.sponsorship.sponsor
