from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, renderers
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from users.models import Profile
from cart.models import Cart
from cart.utils import create_customer_and_order
from cart.forms import PhoneNumber
import json


class CartAPI(APIView):
    """
    Single API to handle cart operations 
    """
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request):
        cart = Cart(request)
        profile = None
        if not request.user.is_anonymous:
            profile = Profile.objects.get(user_id=request.user.id)
            # Підставляємо в input номер телефону користувача
            form = PhoneNumber(
                initial={'phone_number': profile.phone_number})
            return Response(data={'in_cart': list(cart.__iter__()), 'to_pay': cart.get_total_price(), 'count': cart.__len__(), 'profile': profile, 'form': form},
                            status=status.HTTP_200_OK, template_name='cart.html')
        form = PhoneNumber()
        return Response(data={'in_cart': list(cart.__iter__()), 'to_pay': cart.get_total_price(), 'count': cart.__len__(), 'profile': profile, 'form': form},
                        status=status.HTTP_200_OK, template_name='cart.html')

    def post(self, request, **kwargs):
        cart = Cart(request)
        if 'remove' in request.data:
            product = request.data['remove']
            cart.remove(product)

        elif 'clear' in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                product=product['product_id'],
                quantity=product['quantity'],
                overide_quantity=product['overide_quantity'] if 'overide_quantity' in product else False
            )
            return Response(data={'len': cart.__len__(), 'to_pay': cart.get_total_price()}, status=status.HTTP_202_ACCEPTED)
        return redirect(reverse_lazy('cart'), permanent=True)


class CheckCartAPI(APIView):
    """ Сторінка перевірки замовлення

    Args:
        APIView (_type_): Сторінка , де замовник може перевірити свої реквізити та замовлення.
        Сплатити за товар, якщо обран варіант оплати на сайті

    Returns:
        Response: _description_
    """

    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer) 

    def get(self, request):
        return redirect('cart')

    def post(self, request):
        cart = Cart(request)
        to_pay = cart.get_total_price()
        if 'to_pay' in request.data:
            return Response(data={'to_pay': str(to_pay)})
        try:
            data = json.loads(request.data['data'])
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if 'До_замовника' in data['delivery']:
            to_pay += 100  # + 100 грн за кур'єра
        return Response(data={'data': data, 'products': list(cart.__iter__()), 'to_pay': to_pay}, template_name='check_order.html', status=status.HTTP_200_OK)


class AcceptCartAPI(APIView):
    """ Отримання замовлення

    Args:
        APIView (_type_): Створення моделі Order та Custumer

    Returns:
        Response:  500, якщо сталася помилка при збереженні даних
        redirect:  якщо замовлення успішно створене
    """
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request):
        return redirect('/')

    def post(self, request):

        if create_customer_and_order(request):
            cart = Cart(request)
            cart.clear()
            return redirect('/', permanent=True)
        return render(request, '404.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
