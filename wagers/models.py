from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.db import models


class Wager(models.Model):
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='wagers_recieved')

    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wagers_given',
                                null=True)

    amount = models.DecimalField('Amount', default=0, max_digits=10,
                                 decimal_places=2, null=True)

    fulfilled = models.BooleanField('Fulfilled?', default=False)

    paid = models.BooleanField('Paid?', default=False)

    remind_date = models.DateField('Remind Date',
                                   default=lambda: date.today() + \
                                        relativedelta(months=1),
                                   null=True)

    wager_text = models.CharField('Wager Text', max_length=500, null=True,
                                  default=None)

    update_text = models.CharField('Update Text', max_length=500, null=True,
                                   default=None, blank=True)

    def decision_date(self):
        if self.remind_date != None:
            return self.remind_date + relativedelta(days=1)

        return None

    def __unicode__(self):
        return '%s' % self.runner
