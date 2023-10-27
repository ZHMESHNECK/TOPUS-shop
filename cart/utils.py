from products.models import MainModel
from users.models import Profile, Customer
from cart.models import Order
import traceback
import json


def create_customer_and_order(request):
    """Створення моделі Customer та Order

    Args:
        request (_type_): Створення моделі Customer та Order
    Returns:
        Bool: True / False
    """
    try:
        data = json.loads(request.data['data'])
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

    except:
        print(traceback.format_exc())
        return False

    # Створення замовлення
    try:
        for id_product, quantity in data['product'].items():
            order = Order()
            order.customer = customer
            order.product = MainModel.objects.get(id=id_product)
            order.quantity = quantity
            order.pickup = list(data['delivery'].keys())[0]
            addres = ''
            if list(data['delivery'].keys())[0] == 'До_замовника':
                courier = data['delivery']['До_замовника']
                for key, value in courier.items():
                    addres += f'{key}: {value}\n'
                order.city = data['delivery']['До_замовника'].get(
                    'Місто')
            else:
                addres = f'{list(data["delivery"].keys())[0]} - {list(data["delivery"].values())[0]}'
            order.adress = addres
            order.pay = data['pay']
            order.save()
    except:
        print(traceback.format_exc())
        return False

    return True
