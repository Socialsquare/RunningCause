from unittest import skip

import requests

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.contrib.auth import get_user_model

from .models import Run, RunkeeperToken
from .runkeeper import create_runs_from_runkeeper
from datetime import timedelta


class TestSyncAllRunsCommand(TestCase):
    pass
#
#    @mock('runkeeper....')
#    def test_syn_all_runs_output(self):
#        out = StringIO()
#        call_command('syncallruns', stdout=out)
#        self.assertIn('XXXXX', out.getvalue())


class TestInputRun(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create(username='test')
        self.test_user.set_password('pass123')
        self.test_user.is_active = True
        self.test_user.save()

    def test_run_model(self):
        yesterday = timezone.now() - timedelta(days=1)
        new_run = Run.objects.create(runner=self.test_user, distance=10,
                                     recorded_time=timedelta(1),
                                     start_date=yesterday)
        self.assertEquals(new_run.start_date, new_run.end_date)
        # TODO: test save too... ;-)

    def test_input_run_post(self):
        self.client.login(username='test', password='pass123')
        data = {
            'distance': '10',
            'start_date': timezone.now().strftime('%Y-%m-%d'),
            'end_date': timezone.now().strftime('%Y-%m-%d'),
            'recorded_time': '00:01:00',
        }
        resp = self.client.post(reverse('runs:input_run'), data,
                                follow=True)
        self.assertRedirects(resp,
                             reverse('runs:user_runs',
                                     kwargs=dict(user_id=self.test_user.id)),
                             302, 200)
        msgs = list(resp.context['messages'])
        self.assertTrue(msgs)
        self.assertEqual('Your run has been added', str(msgs[0]))


class TestRunkeeper(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(username='test')
        self.test_user.set_password('pass123')
        self.test_user.is_active = True
        self.test_user.save()
        self.token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
        RunkeeperToken.objects.create(runner=self.test_user,
                                      access_token=self.token)

    @skip("WIP")
    def test_create_runs_from_runkeeper(self):
        """
        
        WIP!
        
        """
        self.assertEqual(0, Run.objects.count())

        # create_runs_from_runkeeper(user_id=self.test_user.id)

        # self.assertEqual(1, Run.objects.count())

        headers = {
            'Authorization': 'Bearer %s' % (self.token, ),
            'Accept': '',
        }
        url = 'https://api.runkeeper.com/user'
        headers['Accept'] = 'application/vnd.com.runkeeper.User+json'
        resp = requests.get(url, headers=headers)
        print resp.status_code
        print resp.headers
        print resp.json()

        user = resp.json()

        url = 'https://api.runkeeper.com' + user['fitness_activities']
        headers['Accept'] = 'application/vnd.com.runkeeper.FitnessActivityFeed+json'
        resp = requests.get(url, headers=headers)
        print resp.status_code
        print resp.headers
        print resp.text

        self.assertDictEqual({}, resp.json())
