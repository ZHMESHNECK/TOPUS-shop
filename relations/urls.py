from relations.views import UserRelationViewSet
from django.urls import path


urlpatterns = [
    path('relations/<int:pk>', UserRelationViewSet.as_view(), name='make_relation')
]
