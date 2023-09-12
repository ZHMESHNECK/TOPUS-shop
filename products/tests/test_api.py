from products.serializers import ClothSerializer
from products.models import Clothes, Rating
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json


class MainApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.item = Clothes.objects.create(
            title='test1', price='150.00', size='S', season='SUMMER', owner=self.user, s_code='123')
        self.item2 = Clothes.objects.create(
            title='test2', price='100.00', size='S', season='test1', s_code='223', discount=30)
        self.item3 = Clothes.objects.create(
            title='test3', price='500.00', size='XL', season='SUMMER', s_code='323')
        Rating.objects.create(user=self.user, item=self.item, rate=4)

    def test_get(self):
        """Перевірка зв'язку з сервером, створення 3-ох записів 
        """
        url = reverse('clothes-list')
        response = self.client.get(url)
        items = Clothes.objects.all().annotate(price_w_dis=F(
            'price')-F('price')/100*F('discount'), views=Count('viewed')).order_by('id')

        serializer_data = ClothSerializer(items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], '4.0')

    def test_search(self):
        """Пошук по декількох полях"""
        url = reverse('clothes-list')
        items = Clothes.objects.filter(id__in=[self.item.id, self.item2.id]).annotate(price_w_dis=F(
            'price')-F('price')/100*F('discount'), views=Count('viewed')).order_by('id')

        response = self.client.get(url, data={'search': 'test1'})
        serializer_data = ClothSerializer(
            items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_order(self):
        """Сортування"""
        url = reverse('clothes-list')
        response = self.client.get(url, data={'ordering': '-price'})
        items = Clothes.objects.filter(
            id__in=[self.item.id, self.item2.id, self.item3.id]).annotate(price_w_dis=F(
                'price')-F('price')/100*F('discount'), views=Count('viewed')).order_by('-price')
        serializer_data = ClothSerializer(
            items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        """Створення"""
        self.assertEqual(3, Clothes.objects.all().count())
        url = reverse('clothes-list')
        data = {
            'title': 'test_create_1',
            'price': 400,
            'category': None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Clothes.objects.all().count())

    def test_update(self):
        """Оновлення"""
        url = reverse('clothes-detail', args=(self.item.id,))

        data = {
            'price': 5000,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.item.refresh_from_db()  # дістаємо з БД оновлену модель
        self.assertEqual(5000, self.item.price)

    def test_delete(self):
        """Видалення"""
        self.assertEqual(3, Clothes.objects.all().count())
        self.client.force_login(self.user)
        url = reverse('clothes-detail', args=(self.item.id,))
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertEqual(2, Clothes.objects.all().count())

    def test_update_not_staff(self):
        """Оновлення запису без прав"""

        self.user2 = User.objects.create(username='test2')
        url = reverse('clothes-detail', args=(self.item.id,))

        data = {

            'price': 5000,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.item.refresh_from_db()
        self.assertEqual(150, self.item.price)

    def test_delete_not_staff(self):
        """Видалення запису без прав"""
        self.user2 = User.objects.create(username='test2')
        self.assertEqual(3, Clothes.objects.all().count())
        self.client.force_login(self.user2)
        url = reverse('clothes-detail', args=(self.item.id,))
        response = self.client.delete(url)
        self.assertEqual(403, response.status_code)
        self.assertEqual(3, Clothes.objects.all().count())

    def test_update_staff_not_owner(self):
        """Оновлення запису в БД админом"""
        self.user3 = User.objects.create(username='test2', is_staff=True)
        url = reverse('clothes-detail', args=(self.item.id,))

        data = {
            'title': self.item.title,
            'description': self.item.description,
            'price': 5000,
            'rate_count': 1
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code, response.data)
        self.item.refresh_from_db()
        self.assertEqual(5000, self.item.price)

    def test_discount(self):
        """Встановлення знижки в 30%"""
        self.user3 = User.objects.create(username='test2', is_staff=True)
        url = reverse('clothes-detail', args=(self.item.id,))

        data = {
            "price": 5000,
            "discount": 30,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code, response.data)
        self.item.refresh_from_db()
        self.assertEqual(5000, self.item.price)
        self.assertEqual(30, self.item.discount)


class RelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user2 = User.objects.create(username='test2')
        self.item = Clothes.objects.create(
            title='test1', price='150.00', s_code='1', size='S', season='SUMMER', owner=self.user)
        self.item2 = Clothes.objects.create(
            title='test2', price='100.00', s_code='2', size='S', season='test1')

    def test_rate(self):
        """Змінення рейтингу
        """
        url = reverse('rating-detail', args=(self.item.id,))

        data = {
            'rate': 2,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = Rating.objects.get(user=self.user, item=self.item)
        self.assertEqual(relation.rate, 2)

    def test_rate_wrong(self):
        """Ставлення невірного рейтингу 
        """
        url = reverse('rating-detail', args=(self.item.id,))

        data = {
            'rate': 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
