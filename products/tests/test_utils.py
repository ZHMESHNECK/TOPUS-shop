from django.test import TestCase
from products.utils import serial_code_randomizer, gen_code
from products.models import Clothes, Category


class UtilsTestCase(TestCase):

    def setUp(self) -> None:

        self.cat = Category.objects.create(cat_name='1', slug='1')
        self.cat2 = Category.objects.create(cat_name='2', slug='2')

        self.item = Clothes.objects.create(
            title='da', price=250, s_code='туе', category=self.cat)
        self.item2 = Clothes.objects.create(
            title='net', price=250, s_code='da', category=self.cat2)

    def test_serial_code_randomizer(self):
        """тест рандомайзера коду
        """
    
        self.item.s_code = serial_code_randomizer(self.item.category)
        self.item2.s_code = serial_code_randomizer(self.item2.category)

        self.assertIn(str(self.item.category.id), self.item.s_code[:2])
        self.assertIn(str(self.item2.category.id), self.item2.s_code[:2])

    def test_gen_code(self):
        """ тест генератору напряму
        """

        self.assertEqual(10, len(gen_code('1')))
        self.assertEqual(10, len(gen_code('10')))
        self.assertEqual(10, len(gen_code('100')))