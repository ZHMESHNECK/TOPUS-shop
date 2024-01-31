from django.test import TestCase, LiveServerTestCase
from users.models import User, Profile
import requests


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='email1@email.email', is_staff=True)
        self.user2 = User.objects.create(
            username='test2', email='email2@email.email', is_staff=True)

    def test_create_profile(self):
        """Перевірка створення профілю
        """
        dd = Profile.objects.all()
        self.assertEqual(len(dd), 2)


class DjoserTestCase(LiveServerTestCase):

    def test_djoser_register_user_corr(self):
        """Надсилання коректних даних користувача для реєстрації
        """
        data = {
            "email": 'da@da.da',
            "username": 'test_user',
            "password": 'qwerty_123',
            "re_password": 'qwerty_123'
        }

        url = self.live_server_url + '/api/auth/users/'
        response = requests.post(url, data=data)
        self.assertEqual(201, response.status_code)

    def test_djoser_register_user_wrong(self):
        """Надсилання невірних даних (пошта) користувача для реєстрації
        """
        data = {
            "email": 's',
            "username": 'test_user2',
            "password": 'qwerty_123',
            "re_password": 'qwerty_123'
        }

        url = self.live_server_url + '/api/auth/users/'
        response = requests.post(url, data=data)
        self.assertEqual(400, response.status_code)
