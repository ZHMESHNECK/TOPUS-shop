from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework import renderers
from products.serializers import *
from products.models import *
from products.permission import IsStaffOrReadOnly
from products.utils import serial_code_randomizer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Count
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist


class ClothviewSet(ModelViewSet):
    queryset = Clothes.objects.filter(is_published=True).annotate(price_w_dis=F('price')-F('price') /
                                                                  100*F('discount'), views=Count('viewed')).order_by('id')
    serializer_class = ClothSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'description', 'season', 'size']
    ordering_fields = ['title', 'price', 'category', 'season', 'size']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))

    def list(self, request, *args, **kwargs):
        response = super(ClothviewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='cloth.html')
        return response

    def retrieve(self, request, pk=None):
        response = super(ClothviewSet, self).retrieve(request, pk)
        if request.accepted_renderer.format == 'html':
            images = Gallery_cloth.objects.filter(clothes_id=pk)
            try:
                rating = Relation.objects.get(
                    user=self.request.user.id, item=pk)
            except ObjectDoesNotExist:
                rating = None
            return Response({'data': response.data, 'images': images, 'rating': rating}, template_name='view_cloth.html')
        return response


class GamingViewSet(ModelViewSet):
    queryset = Gaming.objects.all().annotate(price_w_dis=F('price')-F('price') /
                                             100*F('discount'), views=Count('viewed')).order_by('id')
    serializer_class = GamingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))

    def list(self, request, *args, **kwargs):
        response = super(GamingViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='game.html')
        return response

    def retrieve(self, request, pk=None):
        response = super(GamingViewSet, self).retrieve(request, pk)
        if request.accepted_renderer.format == 'html':
            images = Gallery_gaming.objects.filter(gaming_id=pk)
            return Response({'data': response.data, 'images': images}, template_name='view_game.html')
        return response


class HomeViewSet(ModelViewSet):
    queryset = Home.objects.all().annotate(price_w_dis=F('price')-F('price') /
                                           100*F('discount'), views=Count('viewed')).order_by('id')
    serializer_class = HomeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))

    def list(self, request, *args, **kwargs):
        response = super(HomeViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='home.html')
        return response

    def retrieve(self, request, pk=None):
        response = super(HomeViewSet, self).retrieve(request, pk)
        if request.accepted_renderer.format == 'html':
            images = Gallery_home.objects.filter(home_id=pk)
            return Response({'data': response.data, 'images': images}, template_name='view_home.html')
        return response


class UserRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'item'
    filterset_fields = ['in_liked']

    def get_object(self):
        obj, _ = Relation.objects.get_or_create(
            user=self.request.user, item_id=self.kwargs['item'])
        return obj


def main(request):
    return render(request, 'main_page.html')
