from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include
from users.views import RegisterView, EmailSendView, ActivateUser, ChangePasswordUser, LoginUser, logout_user, ForgotPassword, PurchaseHistoryApiView, view_topus_team, render404, ProfileViewSet
from relations.views import FavouriteViewSet, HistoryAPI, HistoryView


urlpatterns = [

    re_path('', include('social_django.urls', namespace='social')),
    re_path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.jwt')),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('success_registration/', EmailSendView.as_view(),
         name='success_send'),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view()),
    path('profile/<str:username>/', ProfileViewSet.as_view(), name='profile'),
    path('password-reset/<str:uidb64>/<str:token>/',
         ChangePasswordUser.as_view(), name='password_reset_confirm'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_pass'),
    path('favourite/', FavouriteViewSet.as_view(), name='favourite'),
    path('add_history/', HistoryAPI.as_view(), name='add_history'),
    path('history/', HistoryView.as_view(), name='history'),
    path('purchase_history/', PurchaseHistoryApiView.as_view(),
         name='purchase_history'),
    path('topus_team/', view_topus_team, name='topus_team'),
    path('404/', render404, name='404')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
