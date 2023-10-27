from rest_framework.test import APITestCase
from rest_framework import status
from django.db.models import Q
from django.urls import reverse
from products.models import Clothes, Category, Gaming
from users.models import User, Profile
from cart.models import Customer, Order
import json

# product: {'3': '1', '4': '2'}
# pay: str
# delivery: {'Самовивіз': '1'}
# До_замовника: {'city': 'city', 'street': 'street', 'building': 'build', 'apartment': '54', 'floor': '-', 'elivator': '-'}


class OrderTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='email1@email.email', is_staff=True)
        self.profile = Profile.objects.get(user=self.user)
        self.cat = Category.objects.create(cat_name='1', slug='cloth')
        self.cat2 = Category.objects.create(cat_name='2', slug='gaming')

        self.item = Clothes.objects.create(
            title='test1', price='150.00', size='S', season='SUMMER', owner=self.user, s_code='123', is_published=True, category=self.cat)
        self.item3 = Clothes.objects.create(
            title='test3', price='500.00', size='XL', season='SUMMER', owner=self.user, s_code='323', is_published=True, category=self.cat)
        self.item4 = Gaming.objects.create(
            title='test4', price='500.00', owner=self.user, s_code='3223', is_published=True, category=self.cat2)

    def test_create_anon_customer(self):
        """ Створення анонимного Customer
        """

        self.assertEqual(0, Customer.objects.all().count())
        url = reverse('accept_order')

        data = {
            'client_info': {
                'email': "admin@admin.admin",
                'first_name': "admin",
                'last_name': "admin",
                'phone_number': "+380000000000",
                'profile': "0",
                'surname': "Володимирович"
            },
            'delivery': {
                'Самовивіз': 1
            },
            'product': {
                str(self.item.id): '2',
                str(self.item3.id): '1'
            },
            'pay': 'При отриманні'
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Customer.objects.all().count())

    def test_create_customer(self):
        """ Створення Customer з існуючим профілем
        """

        self.assertEqual(0, Customer.objects.all().count())
        url = reverse('accept_order')

        data = {
            'client_info': {
                'email': "admin@admin.admin",
                'first_name': "admin",
                'last_name': "admin",
                'phone_number': "+380000000000",
                'profile': self.profile.id,
                'surname': "Володимирович"
            },
            'delivery': {
                'Самовивіз': 1
            },
            'product': {
                str(self.item.id): '2',
                str(self.item3.id): '1'
            },
            'pay': 'При отриманні'
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Customer.objects.all().count())

    def test_create_bad_customer(self):
        """ Створення Customer з невірними данними
        """

        self.assertEqual(0, Customer.objects.all().count())
        url = reverse('accept_order')

        data = {
            'client_info': {
                'email': "",
                'first_name': "",
                'last_name': "",
                'phone_number': "",
                'profile': "",
                'surname': ""
            },
            'delivery': {
                'Самовивіз': 1
            },
            'product': {
                str(self.item.id): '2',
                str(self.item3.id): '1'
            },
            'pay': 'При отриманні'
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR,
                         response.status_code)
        self.assertEqual(0, Customer.objects.all().count())

    def test_order_from_shop(self):
        """ Замовлення - з магазину
        """
        self.assertEqual(0, Order.objects.all().count())
        url = reverse('accept_order')

        data = {
            'client_info': {
                'email': "admin@admin.admin",
                'first_name': "admin",
                'last_name': "admin",
                'phone_number': "+380000000000",
                'profile': self.profile.id,
                'surname': "Володимирович"
            },
            'delivery': {
                'Самовивіз': 1
            },
            'product': {
                str(self.item.id): '2',
                str(self.item3.id): '1'
            },
            'pay': 'При отриманні'
        }

        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Order.objects.all().count())
        self.assertEqual('Самовивіз', Order.objects.filter(
            Q(customer=Customer.objects.get(profile=self.profile)) & Q(product=self.item))[0].pickup)

    def test_order_courier(self):
        """ Замовлення - ку`єр
        """
        self.assertEqual(0, Order.objects.all().count())
        url = reverse('accept_order')

        data = {
            'client_info': {
                'email': "admin@admin.admin",
                'first_name': "admin",
                'last_name': "admin",
                'phone_number': "+380000000000",
                'profile': self.profile.id,
                'surname': "Володимирович"
            },
            'delivery': {'До_замовника':
                         {'city': 'city', 'street': 'street', 'building': 'build', 'apartment': '54', 'floor': '-', 'elivator': '-'}},
            'product': {
                str(self.item.id): '2',
                str(self.item3.id): '1'
            },
            'pay': 'При отриманні'
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Order.objects.all().count())
        self.assertEqual('city: city\nstreet: street\nbuilding: build\napartment: 54\nfloor: -\nelivator: -\n', Order.objects.filter(
            Q(customer=Customer.objects.get(profile=self.profile)) & Q(product=self.item))[0].adress)
