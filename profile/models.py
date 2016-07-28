from django.db import models
from django.contrib import auth
from django.db.models import Sum
from django.utils.translation import ugettext as _
from django.contrib.staticfiles.templatetags.staticfiles import static

from cloudinary.models import CloudinaryField

from challenges.models import Challenge


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

    newsletter = models.BooleanField('Newsletter?', default=False)

    subscribed = models.BooleanField('Subscribed to emails?', default=True)

    stripe_customer_id = models.CharField('Stripe Customer Id', max_length=200,
                                          null=True, blank=True, default=None,
                                          db_index=True)

    greeted = models.BooleanField('Greeted?', default=False)

    picture = CloudinaryField(_('Picture'), null=True, blank=True, default=None)

    objects = MasangaUserManager()

    @property
    def is_runner(self):
        return self.runs.all().exists() or \
            self.sponsorships_recieved.all().exists() or \
            self.challenges_recieved.all().exists()

    @property
    def is_sponsor(self):
        return self.sponsorships_given.all().exists() or \
            self.challenges_given.all().exists()

    @property
    def amount_earned(self):
        spship_amount = self.sponsorships_recieved.all()\
            .aggregate(a_sum=Sum('amount_paid'))['a_sum'] or 0
        challenges_amount = self.challenges_recieved.filter(status='paid')\
            .aggregate(a_sum=Sum('amount'))['a_sum'] or 0
        return spship_amount + challenges_amount

    @property
    def amount_donated(self):
        spship_amount = self.sponsorships_given.all()\
            .aggregate(a_sum=Sum('amount_paid'))['a_sum'] or 0
        challenges_amount = self.challenges_given.filter(status='paid')\
            .aggregate(a_sum=Sum('amount'))['a_sum'] or 0
        return spship_amount + challenges_amount

    @property
    def amount_owed(self):
        sponsorships = self.sponsorships_given.all()
        owed_on_sponsorships = sum([
            s.total_amount - s.amount_paid
            for s in sponsorships
        ])
        challenges = self.challenges_given.filter(status=Challenge.CONFIRMED)
        owed_on_challenges = challenges.aggregate(sum=Sum('amount'))['sum'] or 0
        return owed_on_sponsorships + owed_on_challenges

    @property
    def picture_url(self, **options):
        default_options = dict({
            'width': 250,
            'height': 250,
            'crop': 'fill'
        })
        options = dict(default_options.items() + options.items())
        if self.picture:
            return self.picture.build_url(**options)
        else:
            return static('img/sports_running-4_simple-black-gradient_128x128.png')
