from products.models import MainModel
from users.models import Profile, Customer
from TOPUS.settings import env
from cart.models import Order
import json


def create_customer_and_order(request):
    """Створення моделі Customer та Order

    Args:
        request (_type_): Створення моделі Customer та Order
    Returns:
        Bool: True / False
    """
    # Зберігаємо данні для надсилання фіскального чеку
    order_data = {}
    try:
        data = request.data['data']
        if isinstance(data, str):
            data = json.loads(data)
        customer = Customer()

        if Profile.objects.filter(id=data['client_info'].get('profile')).exists():
            customer.profile = Profile.objects.get(
                id=data['client_info'].get('profile'))
        customer.first_name = data['client_info'].get('first_name')
        customer.last_name = data['client_info'].get('last_name')
        customer.surname = data['client_info'].get('surname')
        customer.phone_number = data['client_info'].get(
            'phone_number')
        customer.email = data['client_info'].get('email')
        customer.save()

        order_data['customer'] = customer
    except:
        return False

    # Створення замовлення
    try:
        order = Order()
        order.customer = customer
        order.pickup = list(data['delivery'].keys())[0]
        address = ''
        if list(data['delivery'].keys())[0] == 'До замовника':
            order.summ_of_pay += int(env('DELIVERY_PRICE'))
            courier = data['delivery']['До замовника']
            for key, value in courier.items():
                address += f'{key}: {value}\n'
            order.city = data['delivery']['До замовника'].get('Місто')
        else:
            address = f'{list(data["delivery"].keys())[0]} - {list(data["delivery"].values())[0]}'
        order.address = address
        order.how_to_pay = data['how_to_pay']
        order.is_pay = data['is_pay']
        order.save()

        product = MainModel.objects.filter(
            id__in=[id for id in data['product'].keys()])

        for id_product, quantity in data['product'].items():
            quantity = int(quantity)
            item = product.get(id=id_product)
            price_w_dis = float(
                item.price - item.price / 100 * item.discount)
            order.products.add(item, through_defaults={
                               'quantity': quantity or 1, 'total': price_w_dis * quantity})
            order.summ_of_pay += price_w_dis * quantity

        order.save()
        order_data['order'] = order.id
    except:
        return False

    return order_data
