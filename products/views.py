from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin
from products.serializers import ClothSerializer, GamingSerializer, RatingSerializer
from products.models import Clothes, Gaming, Rating
from products.permission import IsStaffOrReadOnly
from products.utils import serial_code_randomizer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.db.models import Avg

class ClothviewSet(ModelViewSet):
    queryset = Clothes.objects.all().annotate(
            rate_count=Avg('main_item__rate')).order_by('id')
    serializer_class = ClothSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'description', 'season', 'size']
    ordering_fields = ['title', 'price', 'category', 'season', 'size']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))


class GamingViewSet(ModelViewSet):
    queryset = Gaming.objects.all()
    serializer_class = GamingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))


class HomeViewSet(ModelViewSet):
    queryset = Gaming.objects.all()
    serializer_class = GamingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))


class UserRatingViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = 'item'

    def get_object(self):
        obj, _ = Rating.objects.get_or_create(
            user=self.request.user, item_id=self.kwargs['item'])
        return obj


def auth(request):
    return render(request, 'oauth.html')  # перенести в новую app
