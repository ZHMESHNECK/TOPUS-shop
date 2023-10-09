from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static
from django.conf import settings
from relations.utils import favourite_rel
from relations.views import main
from products.views import ClothviewSet, GamingViewSet, HomeViewSet

from django.urls import path

router = SimpleRouter()
router.register(r'cloth', ClothviewSet)
router.register(r'gaming', GamingViewSet)
router.register(r'for_home', HomeViewSet)


urlpatterns = [
    path('',  main),
    path('add_to_fav/<int:pk>', favourite_rel, name='add_to_fav')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
