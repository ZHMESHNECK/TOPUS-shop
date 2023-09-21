from rest_framework.routers import SimpleRouter
from products.views import ClothviewSet, UserRelationViewSet, GamingViewSet, HomeViewSet
from products.views import main

from django.urls import path

router = SimpleRouter()
router.register(r'clothes', ClothviewSet)
router.register(r'gaming', GamingViewSet)
router.register(r'for_home', HomeViewSet)
router.register(r'relation', UserRelationViewSet)
# тут должны быть роутеры


urlpatterns = [
    path('',  main)
]


urlpatterns += router.urls
