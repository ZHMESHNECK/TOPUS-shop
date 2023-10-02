from rest_framework.routers import SimpleRouter
from products.views import ClothviewSet, GamingViewSet, HomeViewSet
from relations.views import main
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

router = SimpleRouter()
router.register(r'cloth', ClothviewSet)
router.register(r'gaming', GamingViewSet)
router.register(r'for_home', HomeViewSet)


urlpatterns = [
    path('',  main),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
