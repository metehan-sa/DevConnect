from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.projects.models import Project

User = get_user_model()


class ProjectsAppTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='projdev', email='proj@example.com', password='Password123!')
        self.project = Project.objects.create(
            title='Test Project Showcase',
            author=self.user,
            description='### Markdown test header\n\nThis is a test project.',
            tags=['Python', 'Django']
        )

    def test_project_list_view(self):
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project Showcase')

    def test_project_detail_view(self):
        response = self.client.get(reverse('projects:detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project Showcase')

    def test_like_toggle_ajax(self):
        self.client.login(username='projdev', password='Password123!')
        like_url = reverse('projects:like', kwargs={'slug': self.project.slug})
        response = self.client.post(like_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['liked'], True)
        self.assertEqual(response.json()['total_likes'], 1)
