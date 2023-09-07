from products.serializers import ClosthSerializer
from django.contrib.auth.models import User
from products.models import Clothes
from django.test import TestCase
from datetime import timedelta, datetime


class ClothSerializerTestCase(TestCase):
    def test_ok(self):
        """тест сериалайзера
        """
        self.user = User.objects.create(username='test2', is_staff=True)
        item = Clothes.objects.create(
            title='da', price=25, s_code='', owner=self.user)
        item2 = Clothes.objects.create(
            title='net', price=55, s_code='da', owner=self.user)
        data = ClosthSerializer([item, item2], many=True).data
        # що чекаемо отримати, та що отримали
        expected_data = [
            {
                'id': item.id,
                'title': "da",
                'description': "",
                'price': "25.00",
                'brand': "",
                'main_image': None,
                's_code': "",
                'date_created': str((item.date_created+timedelta(hours=3))).split('.')[0],
                'is_published': False,
                'size': "",
                'season': "",
                'department': "",
                'category': None,
                'owner': item.owner.id
            },
            {
                'id': item2.id,
                'title': "net",
                'description': "",
                'price': "55.00",
                'brand': "",
                'main_image': None,
                's_code': "da",
                'date_created': str((item2.date_created+timedelta(hours=3))).split('.')[0],
                'is_published': False,
                'size': "",
                'season': "",
                'department': "",
                'category': None,
                'owner': item2.owner.id
            }
        ]
        self.assertEqual(expected_data, data)
