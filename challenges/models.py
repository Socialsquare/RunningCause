import uuid
import json
from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ChallengeManager(models.Manager):
    def create_for_challenge(self, challenge_request, **kwargs):
        proposed = json.loads(challenge_request.proposed_challenge)
        proposed.update(kwargs)
        instance = self.model(sponsor=challenge_request.sponsor,
                              runner=challenge_request.runner,
                              amount=proposed['amount'],
                              end_date=proposed['end_date'],
                              challenge_text=proposed['challenge_text'])
        instance.save()
        return instance


class Challenge(models.Model):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    DECLINED = 'declined'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    STATUS_CHOICES = (
        (ACTIVE, _('active')),
        (COMPLETED, _('completed')),
        (DECLINED, _('declined')),
        (CONFIRMED, _('confirmed')),
        (PAID, _('paid')),
    )
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='challenges_recieved',
                               null=False)

    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='challenges_given',
                                null=False)

    amount = models.DecimalField('Amount', default=0, max_digits=10,
                                 decimal_places=2, null=False)

    end_date = models.DateField('End Date', default=end_date_default,
                                null=False, db_index=True)

    challenge_text = models.CharField('Challenge Text',
                                      max_length=500,
                                      null=False,
                                      default='')

    runner_msg = models.CharField('Feedback message', max_length=500,
                                   null=True, default=None, blank=True)

    sponsor_msg = models.CharField('Feedback message', max_length=500,
                                   null=True, default=None, blank=True)

    status = models.CharField(choices=STATUS_CHOICES, default=ACTIVE,
                              max_length=10, null=False, db_index=True)

    objects = ChallengeManager()

    def get_feedback_url(self):
        return settings.BASE_URL + reverse('challenges:feedback_challenge',
                                           kwargs={'challenge_id': self.id})

    def __unicode__(self):
        return '%s challenges %s ending %s' % (
            self.sponsor,
            self.runner,
            self.end_date
        )


class ChallengeRequest(models.Model):
    NEW = 'new'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
        (NEW, 'new'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
    )
    runner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='ingoing_challenge_requests')
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='outgoing_challenge_requests')
    created_dt = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4,
                             unique=True, db_index=True, null=False,
                             editable=False, primary_key=False)
    challenge = models.ForeignKey(Challenge, null=True)
    proposed_challenge = models.TextField()  # json field
    status = models.CharField(choices=STATUS_CHOICES, default=NEW,
                              max_length=10, null=False, db_index=True)

    def __unicode__(self):
        return '%s (->) %s' % (self.sponsor, self.runner)
