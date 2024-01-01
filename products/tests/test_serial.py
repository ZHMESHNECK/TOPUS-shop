from products.serializers import ClothSerializer
from products.models import Clothes
from relations.models import Relation
from users.models import User
from django.db.models import F, Count, Q
from django.test import TestCase
from datetime import timedelta


# 3 -  Літній час, 2 - зимний час
time_zone = 2


class ClothSerializerTestCase(TestCase):
    def test_ok(self):
        """тест сериалайзера
        """
        user1 = User.objects.create(
            username='test1', is_staff=True, email='email1@email.email')
        user2 = User.objects.create(
            username='test2', is_staff=True, email='email2@email.email')
        user3 = User.objects.create(
            username='test3', is_staff=True, email='email3@email.email')

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

        items = Clothes.objects.all().annotate(price_w_dis=F('price')-F('price') /
                                               100*F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5)))).order_by('id')
        data = ClothSerializer(items, many=True).data
        # print(f'data {data}')
        # що чекаемо отримати, та що отримали
        expected_data = [
            {
                'id': item.id,
                'price_w_dis': '200.00',
                'views': '3',
                'absolute_url': item.get_absolute_url(),
                'title': 'da',
                'description': '',
                'price': '250.00',
                'brand': '',
                'main_image': '/media/category_photo/no-image-icon.png',
                's_code': item.s_code,
                'date_created': (item.date_created+timedelta(hours=time_zone)).strftime('%Y-%m-%d %H:%M'),
                'discount': 20,
                'rating': '3.7',
                'size': '',
                'season': '',
                'department': '',
                'category': None,
                'in_liked': [],
            },
            {
                'id': item2.id,
                'price_w_dis': '550.00',
                'views': '2',
                'absolute_url': item2.get_absolute_url(),
                'title': 'net',
                'description': '',
                'price': '550.00',
                'brand': '',
                'main_image': '/media/category_photo/no-image-icon.png',
                's_code': item2.s_code,
                'date_created': (item2.date_created+timedelta(hours=time_zone)).strftime('%Y-%m-%d %H:%M'),
                'discount': 0,
                'rating': '3.5',
                'size': '',
                'season': '',
                'department': '',
                'category': None,
                'in_liked': [],
            }
        ]
        # print(f'serial {expected_data}')
        self.assertEqual(expected_data, data)
