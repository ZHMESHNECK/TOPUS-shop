from django.conf import settings
from django.db import models
from products.models import MainModel
from users.models import Customer


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
                "Ціна": float(product.price) if not product.discount else float(product.price - product.price / 100 * product.discount)
            }
        if overide_quantity:
            self.cart[str(product.id)]['Кількість'] = quantity
        else:
            self.cart[str(product.id)]['Кількість'] += quantity
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
        products = MainModel.objects.filter(
            id__in=self.cart.keys()).select_related('category')
        for product in products:
            self.cart[str(product.id)]['Товар'] = product

        for item in self.cart.values():
            item['Ціна'] = item['Ціна']
            item['Всього'] = round(item['Ціна'] * item['Кількість'], 1)

            yield item

    def __len__(self):
        """Кількість товару у кошику
        """
        return sum(item['Кількість'] for item in self.cart.values())

    def get_total_price(self):
        return round(sum(item['Ціна'] * item['Кількість'] for item in self.cart.values()), 1)

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
        ('Виконане', 'Виконане'),
        ('Відмінено', 'Відмінено')
    )
    PAY = (
        ('При отриманні', 'При отриманні'),
        ('На сайті', 'На сайті'),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name='Замовник')
    product = models.ForeignKey(
        MainModel, on_delete=models.CASCADE, verbose_name='Товар')
    pickup = models.CharField('Спосіб доставки', default='---', max_length=50)
    city = models.CharField('Місто', blank=True,
                            max_length=100, default='Не вказано')
    adress = models.TextField('Адресса', blank=True, max_length=100)
    quantity = models.PositiveSmallIntegerField('Кількість', default=1)
    ordered_date = models.DateTimeField('Дата', auto_now_add=True)
    how_to_pay = models.CharField(
        'Спосіб оплати', max_length=50, choices=PAY, default='-')
    is_pay = models.BooleanField('Сплачено', default=False)
    item_price = models.DecimalField(
        'Вартість', max_digits=7, decimal_places=2, default=0)
    summ_of_pay = models.DecimalField(
        'Всього', max_digits=7, decimal_places=2, default=0)
    status = models.CharField('Статус',
                              max_length=50, choices=STATUS_ORDER, default='Прийнято')

    def __str__(self):
        return f'Замовлення: №{self.id}'

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
