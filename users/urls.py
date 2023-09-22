from users.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include


urlpatterns = [

    re_path('', include('social_django.urls', namespace='social')),
    re_path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.jwt')),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('success_registration/', EmailSentView.as_view(), name='success_registration'),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view()),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
