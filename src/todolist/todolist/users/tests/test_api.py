from django.contrib import auth
from django.test import TestCase, client
from django.urls import reverse
from todolist.users.factory_models import UserFactory


class TestLoginAPIView(TestCase):
    def setUp(self):
        self.client = client.Client()

    def login_user(self):
        self.user = UserFactory(username='test', password='test')
        data = {
            'username': self.user.username,
            'password': 'test'
        }
        resp = self.client.post(reverse('login'), data=data, content_type='application/json')
        return resp

    def test_successful_login(self):
        """It will check if we can log in with a user"""
        resp = self.login_user()
        self.assertEqual(resp.status_code, 200)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_login(self):
        """It will check if we can log in with a user"""
        user = UserFactory(username='test', password='test')
        data = {
            'username': user.username,
            'password': 'test2'
        }
        resp = self.client.post(reverse('login'), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 401)

    def test_logout(self):
        self.login_user()
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 200)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)