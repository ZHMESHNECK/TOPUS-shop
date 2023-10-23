from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, renderers
from django.shortcuts import redirect
from cart.models import Cart
from users.models import Profile


# https://www.youtube.com/watch?v=PgCMKeT2JyY&list=PL4FE-nQjkZLyw4pJ7s3kl_fThbTmPdZKd&index=1


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
        return Response(data={'in_cart': list(cart.__iter__()), 'to_pay': cart.get_total_price(), 'count': cart.__len__(), 'profile': profile},
                        status=status.HTTP_200_OK, template_name='cart.html')

    def post(self, request, **kwargs):
        cart = Cart(request)
        if "remove" in request.data:
            product = request.data["remove"]
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
            return Response(data={'len': cart.__len__()}, status=status.HTTP_202_ACCEPTED)

        return redirect('cart', permanent=True)


class AcceptCartAPI(APIView):
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def post(self, request):
        print(request)
        print('da')
        pass
