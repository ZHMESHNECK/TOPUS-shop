from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from cart.serializers import CartSerializer
from cart.models import Cart
import json

# https://pocoz.gitbooks.io/django-v-primerah/content/glava-7-sozdanie-internet-magazina/sozdanie-korzini/ispolzovanie-sessii-django.html
# https://dev.to/nick_langat/building-a-shopping-cart-using-django-rest-framework-54i0
# https://www.youtube.com/watch?v=PgCMKeT2JyY&list=PL4FE-nQjkZLyw4pJ7s3kl_fThbTmPdZKd&index=1


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"У кошику:": list(cart.__iter__()),
             "До сплати:": cart.get_total_price()},
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        cart = Cart(request)
        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                product=product["product_id"],
                quantity=product["quantity"],
                overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
            )

        return Response(
            {"message": "Кошик оновлен"},
            status=status.HTTP_202_ACCEPTED)
