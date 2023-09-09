from django.test import TestCase
from products.utils import serial_code_randomizer, set_rating
from products.models import Clothes, Category, Rating, User


class UtilsTestCase(TestCase):

    def setUp(self) -> None:
        user1 = User.objects.create(username='test1', is_staff=True)
        user2 = User.objects.create(username='test2', is_staff=True)
        user3 = User.objects.create(username='test3', is_staff=True)

        self.cat = Category.objects.create(cat_name='1', slug='1')
        self.cat2 = Category.objects.create(cat_name='2', slug='2')

        self.item = Clothes.objects.create(
            title='da', price=250, s_code='туе', category=self.cat)
        self.item2 = Clothes.objects.create(
            title='net', price=250, s_code='da', category=self.cat2)

        Rating.objects.create(user=user1, item=self.item, rate=5)
        Rating.objects.create(user=user2, item=self.item, rate=3)
        Rating.objects.create(user=user3, item=self.item, rate=4)

    def test_generator(self):
        """тест генератора"""

        self.assertEqual(10, len(serial_code_randomizer(None)))
        self.assertEqual('1', serial_code_randomizer(self.item.category)[0])
        self.assertEqual('2', serial_code_randomizer(self.item2.category)[0])

    def test_set_rate(self):
        set_rating(self.item)
        self.item.refresh_from_db()
        self.assertEqual('4.0', str(self.item.rating))
