from django.test import TestCase
from products.models import Clothes, Category
from users.serializers import PurchaseHistorySerializer
from users.models import User, Customer
from cart.models import Order
from datetime import timedelta

# 3 -  Літній час, 2 - зимний час
time_zone = 2


class PurchaseHistorySerializerTestCase(TestCase):
    def test_ok(self):
        """ тест серіалайзера
        """

        user1 = User.objects.create(
            username='test1', is_staff=True, email='email1@email.email')
        customer = Customer.objects.create(first_name='name', last_name='last_name',
                                           surname='surname', phone_number='+380507830000', email='test@test.test')
        category = Category.objects.create(cat_name='Одежа', slug='cloth')
        item = Clothes.objects.create(
            title='da', price=250, s_code='', owner=user1, category=category)
        item2 = Clothes.objects.create(
            title='net', price=550, s_code='da', owner=user1, category=category)

        order = Order.objects.create(
            customer=customer, pickup='Самовивіз', how_to_pay='При отриманні', is_pay=True, summ_of_pay=800)
        order.products.set([item, item2])
        data = PurchaseHistorySerializer(order).data
        # print(f'data {data}')
        expected_data = [
            {
                'id': order.id,
                'email': customer.email,
                'phone_number': f'+{customer.phone_number.country_code}{customer.phone_number.national_number}',
                'fio': f'{customer.last_name} {customer.first_name} {customer.surname}',
                'products': [{
                    'product_image': item.main_image.url,
                    'product_url': item.get_absolute_url(),
                    'product_title': item.title,
                    'product_quantity': 1,
                    'product_price': float(item.price),
                    'product_total': float(item.price)
                },
                    {
                    'product_image': item2.main_image.url,
                    'product_url': item2.get_absolute_url(),
                    'product_title': item2.title,
                    'product_quantity': 1,
                    'product_price': float(item2.price),
                    'product_total': float(item2.price)
                }
                ],
                'ordered_date': (order.ordered_date + timedelta(hours=time_zone)).strftime('%d-%m-%Y'),
                'pickup': order.pickup,
                'city': order.city,
                'address': order.address,
                'how_to_pay': order.how_to_pay,
                'is_pay': order.is_pay,
                'summ_of_pay': format(order.summ_of_pay, '.2f'),
                'status': order.status,
                'customer': customer.id
            }
        ]
        # print(expected_data)
        self.assertEqual(expected_data, [data])
