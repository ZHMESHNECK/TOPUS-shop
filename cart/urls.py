from django.urls import path
from cart.views import CartAPI


urlpatterns = [
    path('', CartAPI.as_view(), name='cart'),
]
