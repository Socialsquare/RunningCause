from django.db import models
import django.contrib.auth as auth
from datetime import timedelta, datetime
import calendar
import sys

class User(auth.models.AbstractUser):
    USERNAME_FIELD = 'username'
    is_runner = models.BooleanField('Is Runner', default=False)
    is_sponsor = models.BooleanField('Is Sponsor?', default=False)

    def update_sponsorships(self):
        for sponsorship in self.sponsorships_recieved.all():
            sponsorship.update_active_payment()

    @property
    def determine_is_runner(self):
        num_runs = len(self.runs.all())
        answer = num_runs > 0
        self.is_runner = answer
        self.save()
        return answer

    @property
    def determine_is_sponsor(self):
        num_sponsorships = len(self.sponsorships_given.all())
        answer = num_sponsorships > 0
        self.is_sponsor = answer
        self.save()
        return answer

class Sponsorship(models.Model):
    runner = models.ForeignKey(User, related_name='sponsorships_recieved')
    sponsor = models.ForeignKey(User, related_name='sponsorships_given')
    rate = models.FloatField('Rate')
    email = models.EmailField('Email', default='masanga@mailinator.com')
    start_date = models.DateField('Start Date', default = datetime.today().date(), editable=False)
    end_date = models.DateField('End Date', default=(datetime.today()+timedelta(weeks=4)).date())
    max_amount = models.IntegerField('Max Amount', default=sys.maxint)
    access_token = models.CharField('Access Token', max_length = 200, default = "")
    active = models.BooleanField('Active', default=True)

    @property
    def is_past_end_date(self):
        if datetime.today().date() > self.end_date:
            active = False
            return True
        return False

    @property
    def active_payment(self):
        active_payment = self.payments.filter(active=True).first()
        if active_payment == None:
            new_payment = Payment(sponsorship=self)
            new_payment.save()
            return new_payment
        return active_payment


    def pay(self):
        for payment in Payment.objects.filter(sponsorship__pk=self.id):
            payment.active = False
            payment.save()
        new_payment = Payment.create(sponsorship=self)

    def update_active_payment(self):
        self.active_payment.update_amount()

    def __unicode__(self):
        return '%s' % self.sponsor

class Run(models.Model):
    runner = models.ForeignKey(User, related_name='runs')
    distance = models.FloatField('Distance', default=1)
    date = models.DateField('Date', default=datetime.today().date())
    source = models.CharField('Source', default="", max_length=200)
    source_id = models.CharField('Source ID', default="", max_length=200)

    def __unicode__(self):
        return'%s' % self.distance

    def save(self, *args, **kwargs):
        self.runner.update_sponsorships()
        super(Run, self).save(*args, **kwargs)

class Payment(models.Model):
    sponsorship = models.ForeignKey(Sponsorship, related_name='payments')
    amount = models.FloatField('Amount', default=0)
    active = models.BooleanField('Active', default=True)
    start_date = models.DateField('Start Date', default = datetime.today().date(), editable=False)
    end_date = models.DateField('End date', default=datetime(datetime.today().year, datetime.today().month+1, 1).date())

    @property
    def has_ended(self):
        return datetime.today().date() >= end_date

    def __unicode__(self):
        return '%s' % self.sponsorship.sponsor

    def calculate_amount(self):
        rate = self.sponsorship.rate
        relevant_runs = self.sponsorship.runner.runs.filter(date__gte=self.start_date,  date__lt=self.end_date)
        print "Num relevant runs: %s" % len(relevant_runs)
        amount = 0
        for run in relevant_runs:
            amount = amount + (run.distance * rate)
            print "Amount: %s" % amount
        print "Final Amount: %s" % amount
        return amount

    def update_amount(self):
        other_payments = self.sponsorship.payments.exclude(pk=self.id)
        previous_amount = 0
        for payment in other_payments:
            previous_amount = previous_amount + payment.amount
        current_amount = self.calculate_amount()
        print current_amount
        self.amount = min(self.sponsorship.max_amount - previous_amount, current_amount)
        self.save()
