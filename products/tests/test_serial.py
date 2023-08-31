from django.test import TestCase
from django.urls import reverse
from products.models import Clothes
from products.serializers import ClosthSerializer
from rest_framework import status


class ClothSerializerTestCase(TestCase):
    def test_ok(self):
        """тест сериалайзера
        """
        item = Clothes.objects.create(title='da', price=25)
        item2 = Clothes.objects.create(title='net', price=55, slug='da')
        data = ClosthSerializer([item, item2], many=True).data
        # що чекаемо отримати, та що отримали
        expected_data = [
            {
                'id': item.id,
                'title': 'da',
                'description': None,
                'price': '25.00',
                'brand': None,
                'slug': '',
                'size': None,
                'season': None,
                'is_published': False,
                'category': None
            },
            {
                'id': item2.id,
                'title': 'net',
                'description': None,
                'price': '55.00',
                'brand': None,
                'slug': 'da',
                'size': None,
                'season': None,
                'is_published': False,
                'category': None
            },
        ]
        self.assertEqual(expected_data, data)