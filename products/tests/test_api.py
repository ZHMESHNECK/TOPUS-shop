from rest_framework.test import APITestCase
from django.urls import reverse
from products.models import Clothes, Gaming
from products.serializers import ClosthSerializer
from rest_framework import status


class MainApiTestCase(APITestCase):

    def setUp(self):
        self.item = Clothes.objects.create(
            title='test1', price='150.00', slug='1', size='S', season='SUMMER')
        self.item2 = Clothes.objects.create(
            title='test2', price='100.00', slug='2', size='S', season='test1')
        self.item3 = Clothes.objects.create(
            title='test3', price='500.00', slug='3', size='XL', season='SUMMER')

    def test_get(self):
        """Перевірка зв'язку з сервером
        перевірка полей в бд та можливості запису моделі одягу (Clothes)
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
        url = reverse('clothes-list')
        response = self.client.get(url, data={'ordering': '-price'})
        serializer_data = ClosthSerializer(
            [self.item3, self.item, self.item2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
