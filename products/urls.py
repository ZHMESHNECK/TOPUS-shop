from rest_framework.routers import SimpleRouter
from products.views import ClothviewSet, UserRatingViewSet
from products.views import main

from django.urls import path

router = SimpleRouter()
router.register(r'cloth', ClothviewSet)
router.register(r'relation', UserRatingViewSet)
# тут должны быть роутеры


urlpatterns = [
    path('',  main)
]


urlpatterns += router.urls
