from django.test import TestCase
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from django.contrib.auth import get_user_model

from runs.models import Run
from .models import Sponsorship


class SponsorshipTest(TestCase):

    def setUp(self):
        self.test_runner = get_user_model().objects.create(username='runner',
                                                           password=123456)
        self.test_sponsor = get_user_model().objects.create(username='sponsor',
                                                            password=123456)

    def test_basic(self):
        start_date = date.today() - relativedelta(weeks=2)
        end_date = date.today() + relativedelta(weeks=2)
        just_right = Sponsorship.objects.create(runner=self.test_runner,
                                                sponsor=self.test_sponsor,
                                                rate=10,
                                                start_date=start_date,
                                                end_date=end_date,
                                                max_amount=150)

        start_date = date.today() - relativedelta(months=1, weeks=2)
        end_date = end_date = date.today() - relativedelta(months=2, weeks=2)
        too_early = Sponsorship.objects.create(runner=self.test_runner,
                                                sponsor=self.test_sponsor,
                                                rate=10,
                                                start_date=start_date,
                                                end_date=end_date,
                                                max_amount=150)

        start_date = date.today() + relativedelta(months=1, weeks=2)
        end_date = date.today() + relativedelta(months=2, weeks=2)
        too_late = Sponsorship.objects.create(runner=self.test_runner,
                                              sponsor=self.test_sponsor,
                                              rate=10,
                                              start_date=start_date,
                                              end_date=end_date,
                                              max_amount=150)

        Run.objects.create(runner=self.test_runner, distance=10)

        self.assertEqual(just_right.total_amount, 100)
        self.assertEqual(too_early.total_amount, 0)
        self.assertEqual(too_late.total_amount, 0)

    def test_total(self):
        """
        Assert sponsorships stopped after paying their full amount.
        """

        start_date = date.today() - relativedelta(weeks=2)
        end_date = date.today() + relativedelta(months = 2)
        actual = Sponsorship.objects.create(runner=self.test_runner,
                                                sponsor=self.test_sponsor,
                                                rate=10,
                                                start_date=start_date,
                                                end_date=end_date,
                                                max_amount=150)

        Run.objects.create(runner=self.test_runner, distance=10)
        self.assertEqual(actual.total_amount, 100)

        Run.objects.create(runner=self.test_runner, distance=10)
        self.assertEqual(actual.total_amount, 150)
