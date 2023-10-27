from django.conf import settings
from django.db import models
from products.models import MainModel
from users.models import Customer
from decimal import Decimal


class Cart(models.Model):
    """Модель кошика
    """ 

    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, overide_quantity=False):
        """ Додати товар до кошика або додати кількість
        """
        product = MainModel.objects.get(id=product)
        if str(product.id) not in self.cart:
            self.cart[str(product.id)] = {
                "Кількість": 0,
                "Ціна": float(product.price)
            }
        if overide_quantity:
            self.cart[str(product.id)]["Кількість"] = quantity
        else:
            self.cart[str(product.id)]["Кількість"] += quantity
        self.save()

    def remove(self, product):
        """Видалення товару з кошика
        """
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебір елементів у кошику та отримання продуктів із бази даних.
        """
        # Отримання товару та додання їх до кошика
        products = MainModel.objects.filter(id__in=self.cart.keys())
        for product in products:
            self.cart[str(product.id)]['Товар'] = product

        for item in self.cart.values():
            item['Ціна'] = Decimal(item['Ціна'])
            item['Всього'] = item['Ціна'] * item['Кількість']

            yield item

    def __len__(self):
        """Кількість товару у кошику
        """
        return sum(item["Кількість"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["Ціна"]) * item["Кількість"] for item in self.cart.values())

    def clear(self):
        # Видалення кошика з сесії
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошик'


class Order(models.Model):
    """Модель замовлення
    """

    STATUS_ORDER = (
        ('Прийнято', 'Прийнято'),
        ('Збирається', 'Збирається'),
        ('Відправлено', 'Відправлено'),
        ('Готове до видачі', 'Готове до видачі'),
        ('Відмінено', 'Відмінено')
    )
    PAY = (
        ('-', '-'),
        ('При_отриманні', 'При_отриманні'),
        ('На_сайті', 'На_сайті'),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name='Користувач')
    product = models.ForeignKey(
        MainModel, on_delete=models.CASCADE, verbose_name='Товар')
    pickup = models.CharField('Спосіб доставки', default='-', max_length=50)
    city = models.CharField('Місто', blank=True,
                            max_length=100, default='Не вказано')
    adress = models.TextField('Адресса', blank=True, max_length=100)
    quantity = models.PositiveSmallIntegerField("Кількість", default=1)
    ordered_date = models.DateTimeField('Дата', auto_now_add=True)
    pay = models.CharField('Оплата', max_length=50, choices=PAY, default='-')
    status = models.CharField('Статус',
                              max_length=50, choices=STATUS_ORDER, default='Прийнято')

    def __str__(self):
        return f'Замовлення: №{self.id}'

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
