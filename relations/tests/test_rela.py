from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from relations.models import Relation
from products.utils import set_rating
from products.models import Clothes, Category
import json


class RelationTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(
            username='test', email='email1@email.email', is_staff=True)
        self.user2 = User.objects.create(
            username='test2', email='email2@email.email')
        self.item = Clothes.objects.create(
            title='test1', price='150.00', s_code='1', size='S', season='SUMMER', owner=self.user)
        self.item2 = Clothes.objects.create(
            title='test2', price='100.00', s_code='2', size='S', season='test1')

        self.cat = Category.objects.create(cat_name='1', slug='1')
        self.cat2 = Category.objects.create(cat_name='2', slug='2')

        Relation.objects.create(user=self.user, item=self.item, rate=5)

    def test_not_ok(self):
        """Тест на спам рейтингу від 1 юзеру.
        Повинен бути на 1 запит більше.
        Працює без переробленої функції get_or_create як в продакшені, але це 'не баг, а фіча'.
        """
        count = set_rating.count
        self.assertEqual('5.0', str(self.item.rating))
        Relation.objects.get_or_create(user=self.user, item=self.item, rate=5)
        Relation.objects.get_or_create(user=self.user, item=self.item, rate=5)
        Relation.objects.get_or_create(user=self.user, item=self.item, rate=5)
        Relation.objects.get_or_create(user=self.user, item=self.item, rate=4)
        self.item.refresh_from_db()
        self.assertEqual('4.5', str(self.item.rating))
        self.assertEqual(count+1, set_rating.count)

    def test_rate(self):
        """Змінення рейтингу
        """
        url = reverse('relation-detail', args=(self.item.id,))

        data = {
            'rate': 2,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = Relation.objects.get(user=self.user, item=self.item)
        self.assertEqual(relation.rate, 2)

    def test_rate_wrong(self):
        """Ставлення невірного рейтингу 
        """
        url = reverse('relation-detail', args=(self.item.id,))

        data = {
            'rate': 6,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_in_liked(self):
        """Ставлення та перевірка 'лайка'"""
        url = reverse('relation-detail', args=(self.item.id,))

        data = {
            'in_liked': True,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = Relation.objects.get(user=self.user, item=self.item)
        self.assertTrue(relation.in_liked)
