from rest_framework.routers import SimpleRouter
from products.views import ClothviewSet, auth
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path


router = SimpleRouter()
router.register(r'cloth', ClothviewSet)
urlpatterns = [

    path('', auth)

]

urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
