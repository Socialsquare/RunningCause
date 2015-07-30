from django import test
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


class TestTools(test.TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(username='testuser')
        self.test_user.set_password('pass123')
        self.test_user.is_active = True
        self.test_user.is_staff = True
        self.test_user.save()

    def test_info_widget(self):
        url = reverse('tools:info_widget')
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_overview(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('tools:overview')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
