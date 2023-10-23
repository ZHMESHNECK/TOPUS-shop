from django.urls import path
from cart.views import CartAPI, AcceptCartAPI


urlpatterns = [
    path('', CartAPI.as_view(), name='cart'),
    path('accept_order', AcceptCartAPI.as_view(), name='accept_order'),

]
