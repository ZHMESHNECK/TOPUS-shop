from django.test import TestCase
from products.utils import serial_code_randomizer, set_rating
from products.models import Clothes, Category, Relation, User


class UtilsTestCase(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='test1', is_staff=True, email='email1@email.email')
        self.user2 = User.objects.create(username='test2', is_staff=True, email='email2@email.email')
        self.user3 = User.objects.create(username='test3', is_staff=True, email='email3@email.email')

        self.cat = Category.objects.create(cat_name='1', slug='1')
        self.cat2 = Category.objects.create(cat_name='2', slug='2')

        self.item = Clothes.objects.create(
            title='da', price=250, s_code='туе', category=self.cat)
        self.item2 = Clothes.objects.create(
            title='net', price=250, s_code='da', category=self.cat2)

        Relation.objects.create(user=self.user1, item=self.item, rate=5)
        Relation.objects.create(user=self.user2, item=self.item)
        Relation.objects.create(user=self.user3, item=self.item)

    def test_generator(self):
        """тест генератора"""

        self.assertEqual(10, len(serial_code_randomizer(None)))
        self.assertEqual('1', serial_code_randomizer(self.item.category)[0])
        self.assertEqual('2', serial_code_randomizer(self.item2.category)[0])

    def test_not_ok(self):
        """Тест на спам рейтингу від 1 юзеру"""
        self.assertEqual(26, set_rating.count)
        self.assertEqual('5.0', str(self.item.rating))
        Relation.objects.get_or_create(user=self.user1, item=self.item, rate=5)
        Relation.objects.get_or_create(user=self.user1, item=self.item, rate=5)
        Relation.objects.get_or_create(user=self.user1, item=self.item, rate=5)
        Relation.objects.get_or_create(user=self.user1, item=self.item, rate=4)
        self.item.refresh_from_db()
        self.assertEqual('4.5', str(self.item.rating))
        self.assertEqual(27, set_rating.count)
