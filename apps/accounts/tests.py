from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsAppTest(TestCase):
    def test_registration_and_profile_signal(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        # Check signal created profile
        self.assertTrue(hasattr(user, 'profile'))

    def test_login_and_logout(self):
        user = User.objects.create_user(username='loginuser', email='login@example.com', password='StrongPassword123!')
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'loginuser',
            'password': 'StrongPassword123!'
        })
        self.assertEqual(login_response.status_code, 302)

        logout_response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(logout_response.status_code, 302)
