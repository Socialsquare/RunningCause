from django.db import models
import django.contrib.auth as auth
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
import sys

class User(auth.models.AbstractUser):
    USERNAME_FIELD = 'username'
    is_public = models.BooleanField('Info public?', default=False)

    # def update_sponsorships(self):
    #     for sponsorship in self.sponsorships_recieved.all():
    #         sponsorship.update_active_payment()

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
    sponsor = models.ForeignKey(User, related_name='sponsorships_given')
    rate = models.FloatField('Rate', default=0)
    # email = models.EmailField('Email', default='masanga@mailinator.com')
    start_date = models.DateField('Start Date', default = date.today(), editable=False)
    end_date = models.DateField('End Date', default=date.today()+relativedelta(months=1))
    max_amount = models.IntegerField('Max Amount', default=sys.maxint)
    access_token = models.CharField('Access Token', max_length = 200, default = "")
    # active = models.BooleanField('Active', default=True)

    @property
    def is_active(self):
        print ""
        print "Today: %s" % date.today()
        print "Starts: %s" % self.start_date
        print "Ends : %s" % self.end_date
        print ""
        if date.today() < self.end_date and date.today() >= self.start_date:
            print "Is active"
            print ""
            return True
        return False

    @property
    def total_amount(self):
        amount = 0
        for run in self.runner.runs.all():
            if run.date > self.start_date and run.date < self.end_date:
                amount = amount + (self.rate * run.distance)
        amount = min(amount, self.max_amount)
        return amount

    # @property
    # def active_payment(self):
    #     active_payment = self.payments.filter(active=True).first()
    #     if not self.is_active:
    #         if active_payment:
    #             active_payment.active = False
    #         return None
    #     if active_payment == None or active_payment.has_ended:
    #         payment_end_date = min(self.end_date, date.today()+relativedelta(months=1))
    #         new_payment = Payment(sponsorship=self, end_date=payment_end_date)
    #         new_payment.save()
    #         print "New payment created!"
    #         print ""
    #         return new_payment
    #     return active_payment

    



    # def pay(self):
    #     for payment in Payment.objects.filter(sponsorship__pk=self.id):
    #         payment.active = False
    #         payment.save()
    #     if (not self.is_active):
    #         new_payment = Payment.create(sponsorship=self)

    # def update_active_payment(self):
    #     current_payment = self.active_payment
    #     if current_payment != None:
    #         current_payment.update_amount()

    def __unicode__(self):
        return '%s' % self.sponsor

class Run(models.Model):
    runner = models.ForeignKey(User, related_name='runs')
    distance = models.FloatField('Distance', default=1)
    date = models.DateField('Date', default=date.today())
    source = models.CharField('Source', default="", max_length=200)
    source_id = models.CharField('Source ID', default="", max_length=200)

    def __unicode__(self):
        return'%s' % self.distance

    # def save(self, *args, **kwargs):
    #     self.runner.update_sponsorships()
    #     super(Run, self).save(*args, **kwargs)


# class Payment(models.Model):
#     sponsorship = models.ForeignKey(Sponsorship, related_name='payments')
#     amount = models.FloatField('Amount', default=0)
#     active = models.BooleanField('Active', default=True)
#     start_date = models.DateField('Start Date', default = date.today(), editable=False)
#     end_date = models.DateField('End date', default=date.today()+relativedelta(months=1))

#     @property
#     def has_ended(self):
#         result = (date.today() >= self.end_date)
#         active = not result
#         return result

#     def __unicode__(self):
#         return '%s' % self.sponsorship.sponsor

#     def calculate_amount(self):
#         rate = self.sponsorship.rate
#         print "Payment start date: %s" % self.start_date
#         print "Payment end date: %s" % self.end_date
#         relevant_runs = self.sponsorship.runner.runs.filter(date__gte=self.start_date,  date__lt=self.end_date)
#         print "Num relevant runs: %s" % len(relevant_runs)
#         amount = 0
#         for run in relevant_runs:
#             amount = amount + (run.distance * rate)
#             print "Amount: %s" % amount
#         print "Final Amount: %s" % amount
#         return amount

#     def update_amount(self):
#         print "Updating amount..."
#         other_payments = self.sponsorship.payments.exclude(pk=self.id)
#         previous_amount = 0
#         for payment in other_payments:
#             previous_amount = previous_amount + payment.amount
#         print "Previous amount: %s" % previous_amount
#         current_amount = self.calculate_amount()
#         print current_amount
#         self.amount = min(self.sponsorship.max_amount - previous_amount, current_amount)
#         self.save()
