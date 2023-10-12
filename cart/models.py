from decimal import Decimal

from django.conf import settings

from products.models import MainModel


class Cart:
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
        """
        Add product to the cart or update its quantity
        """
        product_id = str(product["id"])
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product["price"])
            }
        if overide_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        """Видалення товару з кошика
        """
        product_id = str(product["id"])

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебір елементів у кошику та отримання продуктів із бази даних.
        """
        product_ids = self.cart.keys()
        # Отримання товару та додання їх до кошика
        products = MainModel.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        # Видалення кошика з сесії
        del self.session[settings.CART_SESSION_ID]
        self.save()
