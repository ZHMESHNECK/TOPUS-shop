from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static
from django.conf import settings
from relations.views import AdToFavAPI
from relations.views import Main_search
from relations.utils import render_404
from products.views import ClothviewSet, GamingViewSet, HomeViewSet

from django.urls import path

router = SimpleRouter()
router.register(r'cloth', ClothviewSet, basename='cloth')
router.register(r'gaming', GamingViewSet, basename='gaming')
router.register(r'for_home', HomeViewSet, basename='home')


urlpatterns = [
    path('', Main_search.as_view(), name='home'),
    path('add_to_fav/<int:pk>', AdToFavAPI.as_view(), name='add_to_fav'),
    path('404', render_404, name='404')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
