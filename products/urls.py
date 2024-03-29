from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static
from django.conf import settings
from relations.views import AdToFavAPI, SearchViewSet, Main
from products.views import ClothviewSet, GamingViewSet, HomeViewSet

from django.urls import path

router = SimpleRouter()
router.register(r'cloth', ClothviewSet, basename='cloth')
router.register(r'gaming', GamingViewSet, basename='gaming')
router.register(r'for_home', HomeViewSet, basename='for_home')


urlpatterns = [
    path('', Main.as_view(), name='home'),
    path('search/', SearchViewSet.as_view(), name='search'),
    path('add_to_fav/<int:pk>', AdToFavAPI.as_view(), name='add_to_fav'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
