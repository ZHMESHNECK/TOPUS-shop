from products.serializers import ClosthSerializer, GamingSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from products.models import Clothes, Gaming
from django.shortcuts import render


class ClothviewSet(ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClosthSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'description', 'season', 'size']
    ordering_fields = ['title', 'price', 'category', 'season', 'size']


class GamingViewSet(ModelViewSet):
    queryset = Gaming.objects.all()
    serializer_class = GamingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model',]


def auth(request):
    return render(request, 'oauth.html')