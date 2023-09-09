from products.serializers import ClothSerializer
from products.models import Clothes, Rating
from django.db.models import Case, Count, When, Avg, F
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from datetime import timedelta, datetime


class ClothSerializerTestCase(TestCase):
    def test_ok(self):
        """тест сериалайзера
        """
        user1 = User.objects.create(username='test1', is_staff=True)
        user2 = User.objects.create(username='test2', is_staff=True)
        user3 = User.objects.create(username='test3', is_staff=True)

        item = Clothes.objects.create(
            title='da', price=250, s_code='', owner=user1, discount=20)
        item2 = Clothes.objects.create(
            title='net', price=550, s_code='da', owner=user2)

        Rating.objects.create(user=user1, item=item, rate=3)
        Rating.objects.create(user=user2, item=item, rate=3)
        Rating.objects.create(user=user3, item=item, rate=3)

        Rating.objects.create(user=user1, item=item2, rate=5)
        Rating.objects.create(user=user2, item=item2, rate=4)
        Rating.objects.create(user=user3, item=item)

        items = Clothes.objects.all().annotate(price_w_dis=F(
            'price')-F('price')/100*F('discount')).order_by('id')
        data = ClothSerializer(items, many=True).data
        # що чекаемо отримати, та що отримали
        expected_data = [
            {
                'id': item.id,
                'title': 'da',
                'description': '',
                'price': '250.00',
                'discount': 20,
                'brand': '',
                'category': None,
                'rating': '3.0',
                'price_w_dis': 200,
                'date_created': (item.date_created+timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
            },
            {
                'id': item2.id,
                'title': 'net',
                'description': '',
                'price': '550.00',
                'discount': 0,
                'brand': '',
                'category': None,
                'rating': '4.5',
                'price_w_dis': 550,
                'date_created': (item2.date_created+timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
            }
        ]
        self.assertEqual(expected_data, data)
