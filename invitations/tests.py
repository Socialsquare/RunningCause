from django import test
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


class TestInvitations(test.TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create(username='testuser')
        self.test_user.set_password('passpass')
        self.test_user.is_active = True
        self.test_user.save()

    def test_invite_via_email_get_not_logged_in(self):
        url = reverse('invitations:invite_via_email')
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        expected = (
            'http://testserver/profile/signuporlogin?next=/invitations/invite-via-email/',
            302
        )
        self.assertEqual(resp.redirect_chain[0], expected)

    def test_invite_via_email_get(self):
        self.client.login(username='testuser', password='passpass')
        url = reverse('invitations:invite_via_email')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_invite_via_email_post(self):
        self.client.login(username='testuser', password='passpass')
        url = reverse('invitations:invite_via_email')
        data = {'email': 'some@email.com'}
        resp = self.client.post(url, data, follow=True)
        expected_url = reverse('runs:user_runs',
                               kwargs=dict(user_id=self.test_user.id))
        self.assertRedirects(resp, expected_url, 302, 200)

        messages = list(resp.context['messages'])
        self.assertTrue(len(messages), 1)

        expected = 'You have just sent invitation to some@email.com'
        self.assertEqual(str(messages[0]), expected)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Masanga Runners invitation')
