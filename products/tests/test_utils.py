from django.test import TestCase
from products.utils import serial_code_randomizer
from products.models import Clothes, Category


class UtilsTestCase(TestCase):

    def setUp(self) -> None:

        self.cat = Category.objects.create(cat_name='1', slug='1')
        self.cat2 = Category.objects.create(cat_name='2', slug='2')

        self.item = Clothes.objects.create(
            title='da', price=250, s_code='туе', category=self.cat)
        self.item2 = Clothes.objects.create(
            title='net', price=250, s_code='da', category=self.cat2)

    def test_generator(self):
        """тест генератора
        """
        self.assertEqual(10, len(serial_code_randomizer(None)))
        self.assertEqual('1', serial_code_randomizer(self.item.category)[0])
        self.assertEqual('2', serial_code_randomizer(self.item2.category)[0])
