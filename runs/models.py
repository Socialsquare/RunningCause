from django.db import models
from django.conf import settings



class Run(models.Model):
    """
    The model for a specific run, or several runs over a period.
    """

    # The runner that ran the run.
    runner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='runs')

    # The distance over the course of the run.
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
    source_id = models.CharField('Source ID', default="", max_length=200)

    def __unicode__(self):
        return'%s' % self.distance
