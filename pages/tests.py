from django import test
from django.core.urlresolvers import reverse


class TestPages(test.TestCase):

    def test_why_join_us(self):
        url = reverse('pages:why_join_us')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Every Step Makes a Difference', resp.content, 1)
