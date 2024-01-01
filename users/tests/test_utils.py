from django.test import TestCase
from users.models import User, Profile


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='email1@email.email', is_staff=True)
        self.user2 = User.objects.create(
            username='test2', email='email2@email.email', is_staff=True)

    def test_create_profile(self):
        dd = Profile.objects.all()
        self.assertEqual(len(dd), 2)
