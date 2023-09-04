from products.models import Clothes, Gaming, Category
from products.serializers import ClosthSerializer
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
import json


class MainApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.item = Clothes.objects.create(
            title='test1', price='150.00', slug='1', size='S', season='SUMMER', owner=self.user)
        self.item2 = Clothes.objects.create(
            title='test2', price='100.00', slug='2', size='S', season='test1')
        self.item3 = Clothes.objects.create(
            title='test3', price='500.00', slug='3', size='XL', season='SUMMER')

    def test_get(self):
        """Перевірка зв'язку з сервером, створення 3-ох записів 
        """
        url = reverse('clothes-list')
        response = self.client.get(url)
        serializer_data = ClosthSerializer(
            [self.item, self.item2, self.item3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_search(self):
        """Пошук по декількох полях"""
        url = reverse('clothes-list')
        response = self.client.get(url, data={'search': 'test1'})
        serializer_data = ClosthSerializer(
            [self.item, self.item2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_order(self):
        """Сортування"""
        url = reverse('clothes-list')
        response = self.client.get(url, data={'ordering': '-price'})
        serializer_data = ClosthSerializer(
            [self.item3, self.item, self.item2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        """Створення"""
        self.assertEqual(3, Clothes.objects.all().count())
        url = reverse('clothes-list')
        data = {
            "title": 'test_create_1',
            "price": 400,
            "slug": 'slug_test_1',
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
            "title": self.item.title,
            "description": self.item.description,
            "price": 5000,
            "brand": self.item.brand,
            "main_image": None,
            "slug": self.item.slug,
            "is_published": False,
            "size": self.item.size,
            "season": self.item.season,
            "category": self.item.category
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
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
            "title": self.item.title,
            "description": self.item.description,
            "price": 5000,
            "brand": self.item.brand,
            "main_image": None,
            "slug": self.item.slug,
            "is_published": False,
            "size": self.item.size,
            "season": self.item.season,
            "category": self.item.category
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(
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
            "title": self.item.title,
            "description": self.item.description,
            "price": 5000,
            "brand": self.item.brand,
            "main_image": None,
            "slug": self.item.slug,
            "is_published": False,
            "size": self.item.size,
            "season": self.item.season,
            "category": self.item.category
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.item.refresh_from_db()
        self.assertEqual(5000, self.item.price)
