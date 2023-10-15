from cart.serializers import CartSerializer
from products.models import Clothes
from users.models import User
from django.test import TestCase
from datetime import timedelta
from cart.models import Cart
import json
from django.urls import reverse
from decimal import Decimal


class CartSerializerTestCase(TestCase):
    def test_ok(self):
        """тест серіалайзера кошика
        """
        self.user1 = User.objects.create(
            username='test1', is_staff=True, email='email1@email.email')

        self.item = Clothes.objects.create(
            title='da', price=250, s_code='', owner=self.user1, discount=20)
        self.item2 = Clothes.objects.create(
            title='net', price=550, s_code='da', owner=self.user1)

        url = reverse('cart')
        self.client.force_login(self.user1)

        data = {
            'product_id': self.item.id,
            'quantity': 2
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        data = {
            'product_id': self.item2.id,
            'quantity': 3
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        self.assertEqual(202, response.status_code)

        response = self.client.get(
            url, content_type='application/json')

        response.status_code
        items = response.data
        data = CartSerializer(items, many=True).instance
        # print(data)
        # що чекаемо отримати, та що отримали
        expected_data = {
            'У кошику:': [
                {'Кількість': 2, 'Ціна': Decimal(
                    '250'), 'Товар': 'da', 'Всього': Decimal('500')},
                {'Кількість': 3, 'Ціна': Decimal(
                    '550'), 'Товар': 'net', 'Всього': Decimal('1650')}],
            'До сплати:': Decimal('2150')}
        # print(expected_data)
        self.assertEqual(expected_data, data)
