from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from products.models import Clothes, Category
from users.models import User
import json


class CartApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='email1@email.email', is_staff=True)
        self.user2 = User.objects.create(
            username='test22', email='email12@email.email', is_staff=True)

        self.cat = Category.objects.create(cat_name='1', slug='cloth')

        self.item = Clothes.objects.create(
            title='test1', price='150.00', size='S', season='SUMMER', owner=self.user, s_code='123', is_published=True, category=self.cat)
        self.item2 = Clothes.objects.create(
            title='test2', price='100.00', size='S', season='test1', owner=self.user2, s_code='223', discount=30, is_published=True, category=self.cat)
        self.item3 = Clothes.objects.create(
            title='test3', price='500.00', size='XL', season='SUMMER', owner=self.user, s_code='323', is_published=True, category=self.cat)

    def test_buy_1_item(self):
        """Додання 1 товару до кошика
        """

        url = reverse('cart')
        self.client.force_authenticate(self.user)

        data = {
            'product_id': self.item.id,
            'quantity': 1
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        cart = self.client.session
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)
        self.assertEqual(cart._session, {'cart': {str(self.item.id): {
                         'Кількість': 1, 'Ціна': float(self.item.price)}}})

    def test_buy_and_check_1_item(self):
        """Додання 1 товару до кошика та його отримання
        """

        url = reverse('cart')
        self.client.force_authenticate(self.user)

        data = {
            'product_id': self.item.id,
            'quantity': 1
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)

        self.assertEqual(202, response.status_code)

        cart = self.client.session

        self.assertEqual({'cart': {str(self.item.id): {'Кількість': 1, 'Ціна': float(
            self.item.price)}}}, cart._session)

    def test_buy_many_and_check(self):
        """Додання декількох товарів до кошика та їх отримання
        """

        url = reverse('cart')
        self.client.force_authenticate(self.user)

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

        cart = self.client.session
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)
        self.assertEqual(cart._session, {'cart': {str(self.item.id): {'Кількість': 2, 'Ціна': float(self.item.price)},
                         str(self.item2.id): {'Кількість': 3, 'Ціна': float(self.item2.price)}}})

    def test_buy_and_change_count(self):
        """Додання 1 товару 5 одиниць до кошика та зменшення до 2-х
        """

        url = reverse('cart')
        self.client.force_authenticate(self.user)

        data = {
            'product_id': self.item.id,
            'quantity': 5
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')
        cart = self.client.session
        self.assertEqual(
            cart._session, {'cart': {str(self.item.id): {'Кількість': 5, 'Ціна': 150.0}}})

        data = {
            'product_id': self.item.id,
            'quantity': 2,
            'overide_quantity': True
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)

        cart = self.client.session
        self.assertEqual(
            cart._session, {'cart': {str(self.item.id): {'Кількість': 2, 'Ціна': 150.0}}})

    def test_remove_1_item(self):
        """Видалення товару з кошика
        """

        url = reverse('cart')
        self.client.force_authenticate(self.user)

        data = {
            'product_id': self.item.id,
            'quantity': 1
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        cart = self.client.session
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)
        self.assertEqual(cart._session, {'cart': {str(self.item.id): {
                         'Кількість': 1, 'Ціна': float(self.item.price)}}})

        data = {
            'remove': self.item.id,
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_301_MOVED_PERMANENTLY,
                         response.status_code)
        cart = self.client.session
        self.assertEqual(cart._session, {'cart': {}})

    def test_buy_1_2_item_del_1(self):
        """Видалення 1-го з 2-х товарів з кошика
        """

        url = reverse('cart')
        self.client.force_authenticate(self.user)

        data = {
            'product_id': self.item.id,
            'quantity': 1
        }
        json_data = json.dumps(data)

        self.client.post(
            url, data=json_data, content_type='application/json')

        data = {
            'product_id': self.item2.id,
            'quantity': 2
        }
        json_data = json.dumps(data)

        self.client.post(
            url, data=json_data, content_type='application/json')

        data = {
            'remove': self.item.id,
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')
        cart = self.client.session

        self.assertEqual(status.HTTP_301_MOVED_PERMANENTLY,
                         response.status_code)
        self.assertEqual(
            cart._session, {'cart': {str(self.item2.id): {'Кількість': 2, 'Ціна': 100.0}}})

    def test_clear(self):
        """Видалення кошика з сессії
        """

        url = reverse('cart')
        self.client.force_authenticate(self.user)

        data = {
            'product_id': self.item.id,
            'quantity': 1
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        cart = self.client.session
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)

        data = {
            'clear': True
        }
        json_data = json.dumps(data)

        response = self.client.post(
            url, data=json_data, content_type='application/json')
        cart = self.client.session
        self.assertEqual(cart._session, {})
