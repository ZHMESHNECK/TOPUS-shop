from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, renderers
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from users.models import Profile
from cart.models import Cart
from cart.utils import create_customer_and_order
from users.forms import ProfileForm
from phonenumbers import PhoneNumber
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
        # Якщо юзер не анонім
        if not request.user.is_anonymous:
            profile = Profile.objects.get(user_id=request.user.id)
            # Підставляємо в input номер телефону користувача
            form = ProfileForm(
                initial={'phone_number': profile.phone_number})
            if len(profile.adress.split()) >= 3:
                adress = profile.adress.split()
                profile.street = adress[0]
                profile.num_street = adress[1]
                profile.apartment = adress[2]
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
        Response:  404 - якщо сталася помилка при збереженні даних & 403 - Немає доступу до цієї сторінки
        redirect:  якщо замовлення успішно створене
    """
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request):
        return Response(template_name='403.html', data={'message': 'Немає доступу до цієї сторінки'}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):

        if create_customer_and_order(request):
            cart = Cart(request)
            cart.clear()
            messages.success(
                request, 'Замовлення успішно створено')
            return redirect('home', permanent=True)
        return Response(template_name='404.html', data={'message': 'При створенні замовлення сталася помилка'}, status=status.HTTP_404_NOT_FOUND)
