import datetime

from django.db import models
from django.conf import settings


class RunkeeperToken(models.Model):
    runner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                  related_name='runkeeper_token')
    access_token = models.CharField(max_length=200, blank=True, null=True,
                                    unique=True, db_index=True)


class Run(models.Model):
    """
    The model for a specific run, or several runs over a period.
    """

    runner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='runs')

    distance = models.FloatField('Distance', default=1)

    # Either the date of the run, or the start of the period over which
    # the runs took place.
    start_date = models.DateField('Date', auto_now_add=True)

    # Either the date of the run, or the end of the period over which
    # the runs took place.
    end_date = models.DateField('End Date', auto_now_add=True)

    # Where the runs were entered, if different from Masanga Runners.
    # Used to keep track of
    # which runs have already been entered.
    source = models.CharField('Source', default="", max_length=200)

    # The id that was assigned to the run on whatever platform it came from,
    # if different
    # from Masanga Runners. Used to keep track of which runs have already
    # been entered.
    source_id = models.CharField('Source ID', default=None, max_length=200,
                                 db_index=True, null=True)

    recorded_time = models.DurationField(default=datetime.timedelta,
                                         null=False)
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True,
                                      null=False)

    def __unicode__(self):
        return'%s' % self.distance
