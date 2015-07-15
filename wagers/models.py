import uuid
from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.db import models


def end_date_default():
    return date.today() + relativedelta(months=3)
remind_date_default = end_date_default

class Wager(models.Model):
    NEW = 'n'
    ACCEPTED = 'a'
    REJECTED = 'r'
    STATUS_CHOICES = (
        (NEW, 'new'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
    )
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='wagers_recieved',
                               null=False)

    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='wagers_given',
                                null=False)

    amount = models.DecimalField('Amount', default=0, max_digits=10,
                                 decimal_places=2, null=False)

    fulfilled = models.BooleanField('Fulfilled?', default=False)

    paid = models.BooleanField('Paid?', default=False)

    end_date = models.DateField('End Date',
                                 default=end_date_default,
                                 null=False, db_index=True)

    wager_text = models.CharField('Wager Text', max_length=500, null=False,
                                  default='')

    update_text = models.CharField('Update Text', max_length=500, null=True,
                                   default=None, blank=True)

    status = models.CharField(choices=STATUS_CHOICES, default=NEW,
                              max_length=1, null=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=False)

    @property
    def remind_date(self):
        if self.end_date:
            return self.end_date - relativedelta(month=1)

    @property
    def decision_date(self):
        if self.end_date is not None:
            return self.end_date + relativedelta(days=1)

    def __unicode__(self):
        return '%s' % self.runner
