from django import test
from django.core.urlresolvers import reverse


class TestPages(test.TestCase):

    def test_contact(self):
        url = reverse('pages:contact')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Every Step Makes a Difference', resp.content, 1)
