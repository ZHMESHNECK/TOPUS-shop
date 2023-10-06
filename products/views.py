from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import renderers
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.messages import get_messages
from django.db.models import F, Count
from products.utils import serial_code_randomizer
from products.serializers import *
from products.models import *
from relations.models import Relation
from relations.utils import accept_post


class ClothviewSet(ModelViewSet):
    queryset = Clothes.objects.filter(is_published=True).annotate(price_w_dis=F('price')-F('price') /
                                                                  100*F('discount'), views=Count('viewed')).order_by('id')
    serializer_class = ClothSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'description', 'season', 'size']
    ordering_fields = ['title', 'price', 'category', 'season', 'size']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))

    def post(self, request, pk):
        request, parametrs = accept_post(self, request, pk)

        response = super(ClothviewSet, self).retrieve(request, pk)
        images = Gallery_cloth.objects.filter(clothes_id=pk)
        relation = Relation.objects.filter(parent__isnull=True, item_id=pk)

        for message in get_messages(request):
            if message.extra_tags == '1':
                parametrs['accept'] = False

        return Response({'data': response.data, 'images': images, 'relation': relation, 'parametrs': parametrs}, template_name='view_cloth.html')

    def list(self, request, *args, **kwargs):
        response = super(ClothviewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='cloth.html')
        return response

    def retrieve(self, request, pk=None):
        response = super(ClothviewSet, self).retrieve(request, pk)
        if request.accepted_renderer.format == 'html':
            images = Gallery_cloth.objects.filter(clothes_id=pk)
            relation = Relation.objects.filter(parent__isnull=True, item_id=pk)
            parametrs = {
                "accept": True
            }
            return Response({'data': response.data, 'images': images, 'relation': relation, 'parametrs': parametrs}, template_name='view_cloth.html')
        return response


class GamingViewSet(ModelViewSet):
    queryset = Gaming.objects.all().annotate(price_w_dis=F('price')-F('price') /
                                             100*F('discount'), views=Count('viewed')).order_by('id')
    serializer_class = GamingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))
        
    def post(self, request, pk):
        request, parametrs = accept_post(self, request, pk)

        response = super(GamingViewSet, self).retrieve(request, pk)
        images = Gallery_gaming.objects.filter(clothes_id=pk)
        relation = Relation.objects.filter(parent__isnull=True, item_id=pk)

        for message in get_messages(request):
            if message.extra_tags == '1':
                parametrs['accept'] = False

        return Response({'data': response.data, 'images': images, 'relation': relation, 'parametrs': parametrs}, template_name='view_game.html')

    def list(self, request, *args, **kwargs):
        response = super(GamingViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='game.html')
        return response

    def retrieve(self, request, pk=None):
        response = super(GamingViewSet, self).retrieve(request, pk)
        if request.accepted_renderer.format == 'html':
            images = Gallery_gaming.objects.filter(clothes_id=pk)
            relation = Relation.objects.filter(parent__isnull=True, item_id=pk)
            parametrs = {
                "accept": True
            }
            return Response({'data': response.data, 'images': images, 'relation': relation, 'parametrs': parametrs}, template_name='view_game.html')
        return response


class HomeViewSet(ModelViewSet):
    queryset = Home.objects.all().annotate(price_w_dis=F('price')-F('price') /
                                           100*F('discount'), views=Count('viewed')).order_by('id')
    serializer_class = HomeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))

    def post(self, request, pk):
        request, parametrs = accept_post(self, request, pk)

        response = super(HomeViewSet, self).retrieve(request, pk)
        images = Gallery_home.objects.filter(clothes_id=pk)
        relation = Relation.objects.filter(parent__isnull=True, item_id=pk)

        for message in get_messages(request):
            if message.extra_tags == '1':
                parametrs['accept'] = False

        return Response({'data': response.data, 'images': images, 'relation': relation, 'parametrs': parametrs}, template_name='view_home.html')

    def list(self, request, *args, **kwargs):
        response = super(HomeViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='home.html')
        return response

    def retrieve(self, request, pk=None):
        response = super(HomeViewSet, self).retrieve(request, pk)
        if request.accepted_renderer.format == 'html':
            images = Gallery_home.objects.filter(clothes_id=pk)
            relation = Relation.objects.filter(parent__isnull=True, item_id=pk)
            parametrs = {
                "accept": True
            }
            return Response({'data': response.data, 'images': images, 'relation': relation, 'parametrs': parametrs}, template_name='view_home.html')
        return response
