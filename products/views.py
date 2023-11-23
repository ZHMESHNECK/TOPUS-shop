from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import renderers
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.messages import get_messages
from django.db.models import F, Count, Q, Prefetch
from products.serializers import *
from products.models import *
from products.utils import serial_code_randomizer
from relations.models import Relation
from relations.utils import accept_post
from utils.pagination import Pagination
from users.models import User

price_with_discount = F('price') - F('price') / 100 * F('discount')


class BaseItemViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['title', 'brand', 'price', 'model']
    ordering = ['-date_created']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]
    pagination_class = Pagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        s_code=serial_code_randomizer(serializer.validated_data['category']))

    def post(self, request, pk):
        request, parametrs = accept_post(self, request, pk)

        response = super(BaseItemViewSet, self).retrieve(request, pk)
        images = self.get_gallery_objects(pk)
        relation = Relation.objects.select_related(
            'item', 'user').filter(parent__isnull=True, item_id=pk).only('item__id','user__id','rate','comment','user__username','parent__id','id')
        answer = Relation.objects.select_related(
            'item', 'user').filter(parent__isnull=False, item_id=pk).only('item__id','user__id','rate','comment','user__username','parent__id','id')
        data_info = self.get_additional_info(response.data)

        # якщо це зміна існуючого відгуку, то блокується кнопка "надіслати"
        for message in get_messages(request):
            if message.extra_tags == '1':
                parametrs['accept'] = False

        return Response({'data': response.data, 'images': images, 'relation': relation, 'answer': answer, 'parametrs': parametrs, 'info': data_info}, template_name='item_view.html')

    def list(self, request, *args, **kwargs):
        response = super(BaseItemViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='list_item_page.html')
        return response

    def retrieve(self, request, pk=None):
        response = super(BaseItemViewSet, self).retrieve(request, pk)
        if request.accepted_renderer.format == 'html':
            images = self.get_gallery_objects(pk)
            relation = Relation.objects.select_related(
                'item', 'user').filter(parent__isnull=True, item_id=pk).only('item__id','user__id','rate','created_at','comment','user__username','id')
            answer = Relation.objects.select_related(
                'item', 'user').filter(parent__isnull=False, item_id=pk).only('item__id','user__id','rate','comment','user__username','parent__id','id')
            data_info = self.get_additional_info(response.data)
            parametrs = {'accept': True}
            return Response({'data': response.data, 'images': images, 'relation': relation, 'answer': answer, 'parametrs': parametrs, 'info': data_info}, template_name='item_view.html')
        return response

    def get_gallery_objects(self, pk):
        raise NotImplementedError('Метод для дітей :)')

    def get_additional_info(self, data):
        raise NotImplementedError('Метод для дітей :)')


class ClothviewSet(BaseItemViewSet):
    queryset = Clothes.objects.all().prefetch_related(Prefetch('in_liked', queryset=User.objects.all().only('id'))).filter(
        is_published=True).annotate(price_w_dis=F('price') - F('price') / 100 * F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5))))
    serializer_class = ClothSerializer

    def get_gallery_objects(self, pk):
        return Gallery_cloth.objects.filter(clothes_id=pk)

    def get_additional_info(self, data):
        return {
            'Пора року': data['season'],
            'Для кого': data['department'],
            'Розмір': data['size']
        }


class GamingViewSet(BaseItemViewSet):
    queryset = Gaming.objects.all().prefetch_related(Prefetch('in_liked', queryset=User.objects.all().only('id'))).filter(
        is_published=True).annotate(price_w_dis=F('price') - F('price') / 100 * F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5))))
    serializer_class = GamingSerializer

    def get_gallery_objects(self, pk):
        return Gallery_gaming.objects.filter(gaming_id=pk)

    def get_additional_info(self, data):
        return {
            'Модель': data['model'],
            'Матеріал': data['material'],
            'Колір': data['color']
        }


class HomeViewSet(BaseItemViewSet):
    queryset = Home.objects.all().prefetch_related(Prefetch('in_liked', queryset=User.objects.all().only('id'))).filter(
        is_published=True).annotate(price_w_dis=F('price') - F('price') / 100 * F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5))))
    serializer_class = HomeSerializer

    def get_gallery_objects(self, pk):
        return Gallery_home.objects.filter(home_id=pk)

    def get_additional_info(self, data):
        return {
            'Для кімнат': data['room_type'],
            'Матеріал': data['material'],
            'Колір': data['color'],
            'Вага': str(data['weight']) + ' кг',
            'Розмір(ВхШхГ), см': data['dimensions'],
        }
