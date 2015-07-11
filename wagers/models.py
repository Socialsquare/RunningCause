from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.contrib.auth import get_user_model


class Wager(models.Model):
    runner = models.ForeignKey(get_user_model(),
                               related_name='wagers_recieved')

    sponsor = models.ForeignKey(get_user_model(), related_name='wagers_given',
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

    class Meta:
        db_table = 'Running_wager'

    def decision_date(self):
        if self.remind_date != None:
            return self.remind_date + relativedelta(days=1)

        return None

    def __unicode__(self):
        return '%s' % self.runner
