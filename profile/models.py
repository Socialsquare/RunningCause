from django.db import models
from django.contrib import auth
from django.db.models import Sum


class MasangaUserManager(auth.models.UserManager):
    def verified_users(self):
        from allauth.account.models import EmailAddress
        not_veryfied = EmailAddress.objects.filter(verified=False)\
            .values_list('user', flat=True)
        return self.model.objects.filter(is_active=True)\
            .exclude(id__in=not_veryfied)


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

    objects = MasangaUserManager()

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
        spship_amount = self.sponsorships_recieved.all()\
            .aggregate(a_sum=Sum('amount_paid'))['a_sum'] or 0
        wagers_amount = self.wagers_recieved.filter(status='paid')\
            .aggregate(a_sum=Sum('amount'))['a_sum'] or 0
        return spship_amount + wagers_amount

    @property
    def amount_donated(self):
        given_spships = self.sponsorships_given.all()
        spship_amount = sum([sp.total_amount for sp in given_spships])
        wagers_amount = self.wagers_given.filter(status='paid')\
            .aggregate(a_sum=Sum('amount'))['a_sum'] or 0
        return spship_amount + wagers_amount

