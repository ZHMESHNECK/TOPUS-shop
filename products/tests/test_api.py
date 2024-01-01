from rest_framework.test import APITestCase
from rest_framework import status
from relations.models import Relation
from products.serializers import ClothSerializer
from products.models import Clothes, Gaming, Home, MainModel, Category
from django.urls import reverse
from django.db.models import Count, F, Q
from users.models import User
import json


class MainApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test', email='email1@email.email', is_staff=True)
        self.user2 = User.objects.create(
            username='test22', email='email12@email.email', is_staff=True)
        self.cat1 = Category.objects.create(cat_name='Одежа', slug='cloth')

        self.item = Clothes.objects.create(
            title='test1', price='150.00', size='S', season='SUMMER', owner=self.user, s_code='123', is_published=True, category=self.cat1)
        self.item2 = Clothes.objects.create(
            title='test2', price='100.00', size='S', season='test1', owner=self.user2, s_code='223', discount=30, is_published=True, category=self.cat1)
        self.item3 = Clothes.objects.create(
            title='test3', price='500.00', size='XL', season='SUMMER', owner=self.user, s_code='323', is_published=True, brand='test1', category=self.cat1)
        self.item4 = Gaming.objects.create(
            title='test4', price='500.00', owner=self.user, s_code='111', is_published=True)
        self.item5 = Home.objects.create(
            title='test5', price='500.00', weight=100, owner=self.user, s_code='222', is_published=True)

        Relation.objects.create(user=self.user, item=self.item, rate=4)

    def test_get(self):
        """Перевірка зв'язку з сервером, створення 3-ох записів 
        """
        url = reverse('cloth-list')
        response = self.client.get(url)
        items = Clothes.objects.all().annotate(price_w_dis=F('price')-F('price') /
                                               100*F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5)))).order_by('-id')

        serializer_data = ClothSerializer(items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0]['id'],
                         response.data['results'][0]['id'])
        self.assertEqual(serializer_data[2]['id'],
                         response.data['results'][2]['id'])
        self.assertEqual(serializer_data[-1]['rating'], '4.0')

    def test_search(self):
        """Пошук по декількох полях
        """
        url = reverse('search')
        items = Clothes.objects.filter(id__in=[self.item.id, self.item3.id]).annotate(price_w_dis=F('price')-F('price') /
                                                                                      100*F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5))))
        response = self.client.get(url, data={'search': 'test1'})
        serializer_data = ClothSerializer(
            items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(serializer_data), len(
            response.data['data']['results']))

    def test_order(self):
        """Сортування
        """
        url = reverse('cloth-list')
        response = self.client.get(url, data={'ordering': '-price'})
        items = Clothes.objects.filter(
            id__in=[self.item.id, self.item2.id, self.item3.id]).annotate(price_w_dis=F('price')-F('price') /
                                                                          100*F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5)))).order_by('-price')
        serializer_data = ClothSerializer(
            items, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0]['id'],
                         response.data['results'][0]['id'])
        self.assertEqual(serializer_data[1]['id'],
                         response.data['results'][1]['id'])
        self.assertEqual(serializer_data[2]['id'],
                         response.data['results'][2]['id'])

    def test_create(self):
        """Створення
        """
        self.assertEqual(3, Clothes.objects.all().count())
        url = reverse('cloth-list')
        data = {
            'title': 'test_create_1',
            'price': 400,
            'category': None
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Clothes.objects.all().count())

    def test_update(self):
        """Оновлення
        """
        url = reverse('cloth-detail', args=(self.item.id,))

        data = {
            'price': 5000,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code, response.data)
        self.item.refresh_from_db()  # дістаємо з БД оновлену модель
        self.assertEqual(5000, self.item.price)

    def test_delete(self):
        """Видалення
        """
        self.assertEqual(3, Clothes.objects.all().count())
        self.client.force_authenticate(self.user)
        url = reverse('cloth-detail', args=(self.item.id,))
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertEqual(2, Clothes.objects.all().count())

    def test_update_not_staff(self):
        """Оновлення запису без прав
        """

        self.user2 = User.objects.create(username='test2')
        url = reverse('cloth-detail', args=(self.item.id,))

        data = {
            'price': 5000,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user2)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.item.refresh_from_db()
        self.assertEqual(150, self.item.price)

    def test_delete_not_staff(self):
        """Видалення запису без прав
        """
        self.user2 = User.objects.create(username='test2')
        self.assertEqual(3, Clothes.objects.all().count())
        self.client.force_authenticate(self.user2)
        url = reverse('cloth-detail', args=(self.item.id,))
        response = self.client.delete(url)
        self.assertEqual(403, response.status_code)
        self.assertEqual(3, Clothes.objects.all().count())

    def test_update_staff_not_owner(self):
        """Оновлення запису в БД админом
        """
        self.user3 = User.objects.create(username='test2', is_staff=True)
        url = reverse('cloth-detail', args=(self.item.id,))

        data = {
            'title': self.item.title,
            'description': self.item.description,
            'price': 5000,
            'rate_count': 1
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.put(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code, response.data)
        self.item.refresh_from_db()
        self.assertEqual(5000, self.item.price)

    def test_discount(self):
        """Встановлення знижки в 30%
        """
        self.user3 = User.objects.create(username='test2', is_staff=True)
        url = reverse('cloth-detail', args=(self.item.id,))

        data = {
            "price": "5000",
            "discount": "30",
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user3)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code, response.data)
        self.item.refresh_from_db()
        self.assertEqual(5000, self.item.price)
        self.assertEqual(30, self.item.discount)

    def test_absolute_url(self):
        """ Перевірка get_absolute_url в усіх моделях
        """
        self.assertEqual(MainModel.get_absolute_url(
            self.item), f'/cloth/{self.item.id}/')
        self.assertEqual(self.item2.get_absolute_url(),
                         f'/cloth/{self.item2.id}/')
        self.assertEqual(self.item4.get_absolute_url(),
                         f'/gaming/{self.item4.id}/')
        self.assertEqual(self.item5.get_absolute_url(),
                         f'/for_home/{self.item5.id}/')
