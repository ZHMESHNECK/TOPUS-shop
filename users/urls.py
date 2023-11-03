from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include
from users.views import *
# from users.utils import PesnolaData


router = SimpleRouter()
router.register(r'profile', ProfileViewSet)

urlpatterns = [

    re_path('', include('social_django.urls', namespace='social')),
    re_path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.jwt')),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('success_registration/', EmailSendView.as_view(),
         name='success_send'),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view()),
    path('password-reset/<str:uidb64>/<str:token>/',
         ChangePasswordUser.as_view(), name='password_reset_confirm'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_pass'),
    # path('save_pers_data/', PesnolaData.as_view(), name='update_profile')
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
