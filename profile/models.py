from django.db import models
from django.contrib import auth


# TODO: check Running_user_groups Running_user_user_permissions
class User(auth.models.AbstractUser):
    USERNAME_FIELD = 'username'

    is_public = models.BooleanField('Info public?', default=False)

    #   This variable is an access token to be used with RunKeeper,
    # if the user has connected with it yet.
    access_token = models.CharField('Access token', max_length=200,
                                    default="", blank=True)

    newsletter = models.BooleanField('Newsletter?', default=False)

    subscribed = models.BooleanField('Subscribed to emails?', default=True)

    stripe_customer_id = models.CharField('Stripe Customer Id', max_length=200,
                                          null=True, blank=True, default=None,
                                          db_index=True)

    greeted = models.BooleanField('Greeted?', default=False)

    class Meta:
        db_table = 'Running_user'

    @property
    def is_runner(self):
        return self.runs.all().exists() or \
            self.sponsorships_recieved.all().exists() or \
            self.wagers_recieved.all().exists()

    @property
    def is_sponsor(self):
        return self.sponsorships_given.all().exists() or \
            self.wagers_given.all().exists()

    @property
    def amount_earned(self):
        rec_spships = self.sponsorships_recieved.all().exclude(sponsor=None)
        return sum([sp.total_amount for sp in rec_spships])

    @property
    def amount_donated(self):
        given_spships = self.sponsorships_given.all().exclude(runner=None)
        return sum([sp.total_amount for sp in given_spships])
