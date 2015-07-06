from django.test import TestCase
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from Running.models import User, Sponsorship, Run


class PaymentTestCase(TestCase):


    def setUp(self):

        User.objects.create(username='runner', password=123456)
        User.objects.create(username='sponsor', password=123456)

    def test_basic(self):

        """If this doesn't work, something has gone very, very wrong. Test dates very simply."""


        just_right = Sponsorship.objects.create(runner=User.objects.get(username='runner'), 
                                                sponsor=User.objects.get(username='sponsor'), 
                                                rate=10, 
                                                start_date=date.today() - relativedelta(weeks=2),
                                                end_date=date.today() + relativedelta(weeks=2),
                                                max_amount=150)
        too_early = Sponsorship.objects.create(runner=User.objects.get(username='runner'), 
                                                sponsor=User.objects.get(username='sponsor'), 
                                                rate=10, 
                                                start_date=date.today() - relativedelta(months=1, weeks=2),
                                                end_date=date.today() - relativedelta(months=2, weeks=2),
                                                max_amount=150)
        too_late = Sponsorship.objects.create(runner=User.objects.get(username='runner'), 
                                                sponsor=User.objects.get(username='sponsor'), 
                                                rate=10, 
                                                start_date=date.today() + relativedelta(months=1, weeks=2),
                                                end_date=date.today() + relativedelta(months=2, weeks=2),
                                                max_amount=150)
        run = Run.objects.create(runner=User.objects.get(username='runner'),
                            distance=10)
        run.save()

        
        self.assertEqual(just_right.total_amount, 100)

        self.assertEqual(too_early.total_amount, 0)

        self.assertEqual(too_late.total_amount, 0)

    def test_total(self):

        """See if sponsorships stop after paying their full amount"""


        just_right = Sponsorship.objects.create(runner=User.objects.get(username='runner'), 
                                                sponsor=User.objects.get(username='sponsor'), 
                                                rate=10, 
                                                start_date=date.today() - relativedelta(weeks=2),
                                                end_date=date.today() + relativedelta(months = 2),
                                                max_amount=150)
       
        first_run = Run.objects.create(runner=User.objects.get(username='runner'),
                            distance=10)
        first_run.save()

        
        self.assertEqual(just_right.total_amount, 100)


        first_run = Run.objects.create(runner=User.objects.get(username='runner'),
                            distance=10)
        first_run.save()

        
        self.assertEqual(just_right.total_amount, 150)

        