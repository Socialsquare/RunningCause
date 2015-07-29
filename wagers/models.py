import uuid
import json
from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


def end_date_default():
    return date.today() + relativedelta(months=3)
remind_date_default = end_date_default


class WagerManager(models.Manager):
    def create_for_challenge(self, wager_request, **kwargs):
        proposed = json.loads(wager_request.proposed_wager)
        proposed.update(kwargs)
        instance = self.model(sponsor=wager_request.sponsor,
                              runner=wager_request.runner,
                              amount=proposed['amount'],
                              end_date=proposed['end_date'],
                              wager_text=proposed['wager_text'])
        instance.save()
        return instance


class Wager(models.Model):
    NEW = 'new'
    COMPLETED = 'completed'
    DECLINED = 'declined'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    STATUS_CHOICES = (
        (NEW, NEW),
        (COMPLETED, COMPLETED),
        (DECLINED, DECLINED),
        (CONFIRMED, CONFIRMED),
        (PAID, PAID),
    )
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='wagers_recieved',
                               null=False)

    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='wagers_given',
                                null=False)

    amount = models.DecimalField('Amount', default=0, max_digits=10,
                                 decimal_places=2, null=False)

    end_date = models.DateField('End Date', default=end_date_default,
                                null=False, db_index=True)

    wager_text = models.CharField('Wager Text', max_length=500, null=False,
                                  default='')

    runner_msg = models.CharField('Feedback message', max_length=500,
                                   null=True, default=None, blank=True)

    sponsor_msg = models.CharField('Feedback message', max_length=500,
                                   null=True, default=None, blank=True)

    status = models.CharField(choices=STATUS_CHOICES, default=NEW,
                              max_length=10, null=False, db_index=True)

    objects = WagerManager()

    @staticmethod
    def get_remind_date_delta():
        return relativedelta(month=1)

    @property
    def remind_date(self):
        if self.end_date:
            return self.end_date - Wager.get_remind_date_delta()

    @staticmethod
    def get_decision_date_delta():
        return relativedelta(days=1)

    @property
    def decision_date(self):
        if self.end_date:
            return self.end_date + Wager.get_decision_date_delta()

    def get_feedback_url(self):
        return settings.BASE_URL + reverse('feedback_wager',
                                           kwargs={'wager_id': self.id})

    def __unicode__(self):
        return '%s' % self.runner


class WagerRequest(models.Model):
    NEW = 'new'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
        (NEW, 'new'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
    )
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='wagers_requested')
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='wagers_requests')
    created_dt = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4,
                             unique=True, db_index=True, null=False,
                             editable=False, primary_key=False)
    wager = models.ForeignKey(Wager, null=True)
    proposed_wager = models.TextField()  # json field
    status = models.CharField(choices=STATUS_CHOICES, default=NEW,
                              max_length=10, null=False, db_index=True)

    def __unicode__(self):
        return '%s (->) %s' % (self.sponsor, self.runner)
