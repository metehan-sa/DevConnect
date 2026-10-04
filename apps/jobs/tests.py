from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.jobs.models import JobPosting

User = get_user_model()


class JobsAppTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jobemployer', email='employer@example.com', password='Password123!')
        self.job = JobPosting.objects.create(
            title='Django Backend Lead',
            company_name='Acme Corp',
            location_type='remote',
            apply_url='https://example.com/apply',
            description='We are hiring a backend lead.',
            author=self.user
        )

    def test_job_list_view(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Backend Lead')

    def test_job_detail_view(self):
        response = self.client.get(reverse('jobs:detail', kwargs={'pk': self.job.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acme Corp')
