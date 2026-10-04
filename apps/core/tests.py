from django.test import TestCase
from django.urls import reverse


class CoreViewsTest(TestCase):
    def test_home_page_status_code_and_template(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertIn('featured_projects', response.context)
        self.assertIn('stats', response.context)
