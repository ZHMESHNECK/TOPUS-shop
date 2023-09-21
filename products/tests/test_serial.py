from products.serializers import ClothSerializer
from products.models import Clothes, Relation
from users.models import User
from django.test import TestCase
from django.db.models import F
from datetime import timedelta


class ClothSerializerTestCase(TestCase):
    def test_ok(self):
        """тест сериалайзера
        """
        user1 = User.objects.create(username='test1', is_staff=True, email='email1@email.email')
        user2 = User.objects.create(username='test2', is_staff=True, email='email2@email.email')
        user3 = User.objects.create(username='test3', is_staff=True, email='email3@email.email')

        item = Clothes.objects.create(
            title='da', price=250, s_code='', owner=user1, discount=20)
        item2 = Clothes.objects.create(
            title='net', price=550, s_code='da', owner=user2)

        Relation.objects.update_or_create(user=user1, item=item, rate=4)
        Relation.objects.update_or_create(user=user2, item=item, rate=3)
        user_item_3 = Relation.objects.update_or_create(user=user3, item=item)
        user_item_3[0].rate = 4
        user_item_3[0].save()

        Relation.objects.update_or_create(user=user1, item=item2, rate=3)
        Relation.objects.update_or_create(user=user1, item=item2, rate=3)
        Relation.objects.update_or_create(user=user2, item=item2, rate=4)
        Relation.objects.update_or_create(user=user3, item=item2)

        items = Clothes.objects.all().annotate(price_w_dis=F(
            'price')-F('price')/100*F('discount')).order_by('id')
        data = ClothSerializer(items, many=True).data
        print(data)
        # що чекаемо отримати, та що отримали
        expected_data = [
            {
                'id': item.id,
                'title': 'da',
                'main_image': None,
                'description': '',
                'price': '250.00',
                'price_w_dis': '200.00',
                's_code': item.s_code,
                'discount': 20,
                'brand': '',
                'category': None,
                'rating': '3.7',
                'size': '',
                'season': '',
                'department': '',
                'date_created': (item.date_created+timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
            },
            {
                'id': item2.id,
                'title': 'net',
                'main_image': None,
                'description': '',
                'price': '550.00',
                'price_w_dis': '550.00',
                's_code': item2.s_code,
                'discount': 0,
                'brand': '',
                'category': None,
                'rating': '3.5',
                'size': '',
                'season': '',
                'department': '',
                'date_created': (item2.date_created+timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
            }
        ]
        print(expected_data)
        self.assertEqual(expected_data, data)
