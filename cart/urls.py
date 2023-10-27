from django.urls import path
from cart.views import *


urlpatterns = [
    path('', CartAPI.as_view(), name='cart'),
    path('check_order', CheckCartAPI.as_view(), name='check_order'),
    path('accept_order', AcceptCartAPI.as_view(), name='accept_order'),

]
