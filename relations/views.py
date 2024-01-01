from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework import status, renderers
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F, Count, Q, Prefetch, Case, When
from relations.serializers import RelationSerializer
from relations.models import Relation
from products.serializers import SearchSerializer
from products.models import MainModel
from products.utils import ProductPriceFilter
from utils.pagination import Pagination
from users.models import User


class UserRelationViewSet(APIView):
    """Створення / змінення відгука на товар

    Args:
        APIView (_type_): _description_

    Returns:
        Response
        Relation: obj
    """
    permission_classes = [IsAuthenticated]
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'item'
    filterset_fields = ['in_liked']
    authentication_classes = [SessionAuthentication]

    def get(self, request, pk):
        return Response(template_name='403.html', data={'message': 'Немає доступу до цієї сторінки'}, status=status.HTTP_403_FORBIDDEN)

    def get_object(self):
        obj, _ = Relation.objects.get_or_create(
            user=self.request.user, item_id=self.kwargs['item'])
        return obj


class Main(APIView):
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request):
        return Response(template_name='main_page.html', status=status.HTTP_200_OK)


class SearchViewSet(ListAPIView):
    """ Search

    Args:
        ListAPIView (_type_): пошук товарів по запиту

    Returns:
        Response: data
    """
    queryset = MainModel.objects.filter(is_published=True).prefetch_related(Prefetch('in_liked', queryset=User.objects.all().only('id'))).annotate(
        price_w_dis=F('price') - F('price') / 100 * F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5))))
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = SearchSerializer
    filterset_class = ProductPriceFilter
    search_fields = ['title', 'description', 'brand']
    ordering_fields = ['price', 'date_created', 'rating']
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    authentication_classes = [SessionAuthentication]
    pagination_class = Pagination

    def get_queryset(self, ordering):
        queryset = super().get_queryset().order_by(ordering)
        return queryset

    def list(self, request):
        query = self.request.query_params.get('search')
        # якщо є заданий параметр сортування то зберігаємо його, інакше за дефолтом ( новинки )
        ordering = self.request.query_params.get('ordering', '-pk')
        queryset = self.get_queryset(ordering)

        # сортування за ціною ( від - до )
        filterset = self.filterset_class(
            self.request.query_params, queryset=queryset)
        queryset = filterset.qs

        if query:
            # якщо довжинна запиту більша за 2, робимо пошук й в опису
            if len(query) >= 3:
                data = queryset.filter(
                    Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query))
            else:
                data = queryset.filter(
                    Q(title__icontains=query) | Q(brand__icontains=query))
            paginated_queryset = self.paginate_queryset(data)
            serializer = SearchSerializer(paginated_queryset, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            message = ''
            if not paginated_response.data['results']:
                message = 'За вашим запитом нічого не знайдено'
            return Response(data=({'data': paginated_response.data, 'message': message}), template_name='list_item_page.html', status=status.HTTP_200_OK)
        messages.error(request, 'При пошуку сталася помилка')
        return redirect('home')


class AdToFavAPI(APIView):
    """ Додає товар до улюбленого чи видаляє з нього якщо товар вже був доданий

    Args:
        request (_type_): запит
        pk (_type_): id користувача

    Returns:
        redirect: login  ( якщо користувач не залогінен )
        Response: True - Додано до бажаного, False - видалено з бажаного
    """

    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def post(self, request, pk, **kwargs):

        # для авторизованих користувачів ( зберігаемо в БД )
        if request.user.is_authenticated:
            item = get_object_or_404(MainModel, pk=pk)
            if item.in_liked.filter(pk=request.user.id).exists():
                item.in_liked.remove(request.user)
                return Response(data={'data': False, 'id': pk}, status=status.HTTP_202_ACCEPTED)
            else:
                item.in_liked.add(request.user)
                return Response(data={'data': True, 'id': pk}, status=status.HTTP_202_ACCEPTED)
        # зберігаемо в сессии
        else:
            liked_products = request.session.get('favourite_products', [])
            item = get_object_or_404(MainModel, pk=pk)
            if pk in liked_products:
                request.session['favourite_products'].remove(pk)
                request.session['favourite_products'] = liked_products
                return Response(data={'data': False, 'id': pk}, status=status.HTTP_202_ACCEPTED)
            else:
                liked_products.insert(0, pk)
                request.session['favourite_products'] = liked_products
                return Response(data={'data': True, 'id': pk}, status=status.HTTP_202_ACCEPTED)


class FavouriteViewSet(ListAPIView):
    """Список доданого в улюблене

    Args:
        ListAPIView (_type_): _description_
    """
    serializer_class = SearchSerializer
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    pagination_class = Pagination

    def get_queryset(self, request):
        list_id_product = request.session.get('favourite_products', [])
        ordering_conditions = [When(id=id_val, then=pos) for pos, id_val in enumerate(
            list_id_product)] if list_id_product else ''
        if request.user.is_anonymous:
            queryset = MainModel.objects.filter(is_published=True, pk__in=list_id_product).prefetch_related('category', Prefetch('in_liked', queryset=User.objects.all().only(
                'id'))).annotate(price_w_dis=F('price') - F('price') / 100 * F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5)))).order_by(Case(*ordering_conditions) if ordering_conditions else 'pk')
        else:
            queryset = MainModel.objects.filter(is_published=True, in_liked=self.request.user.id).prefetch_related('category', Prefetch('in_liked', queryset=User.objects.all().only(
                'id'))).annotate(price_w_dis=F('price') - F('price') / 100 * F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5)))).order_by(Case(*ordering_conditions) if ordering_conditions else 'pk')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SearchSerializer(paginated_queryset, many=True)
        # Отримуємо відповідь від пагінації
        paginated_response = self.get_paginated_response(serializer.data)
        return Response(data=({'data': paginated_response.data}), template_name='list_item_page.html', status=status.HTTP_200_OK)


class HistoryAPI(APIView):
    """Додання товарів в історію переглянутого

    Args:
        APIView (_type_): _description_
    """
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def post(self, request):
        viewed_products = request.session.get('viewed_products', [])
        if request.data not in viewed_products:
            viewed_products.insert(0, request.data)
            request.session['viewed_products'] = viewed_products
        else:
            viewed_products.remove(request.data)
            viewed_products.insert(0, request.data)
            request.session['viewed_products'] = viewed_products
        return Response(status=status.HTTP_200_OK)


class HistoryView(ListAPIView):
    """Вивід списку історії переглянутих товарів

    Args:
        ListAPIView (_type_): _description_

    Returns:
        _type_: _description_
    """

    serializer_class = SearchSerializer
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    pagination_class = Pagination

    def get_queryset(self):
        viewed_product_ids = self.request.session.get('viewed_products', [])
        ordering_conditions = [When(id=id_val, then=pos) for pos, id_val in enumerate(
            viewed_product_ids)] if viewed_product_ids else ''  # Якщо список товарів не пустий, інакше ""
        queryset = MainModel.objects.filter(id__in=viewed_product_ids, is_published=True).prefetch_related('category',
                                                                                                           Prefetch(
                                                                                                               'in_liked', queryset=User.objects.only('id'))
                                                                                                           ).annotate(
            price_w_dis=F('price') - F('price') / 100 * F('discount'),
            views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5)))
        ).order_by(Case(*ordering_conditions) if ordering_conditions else 'pk')  # Сортування за переглядами якщо вони е, інакше за "pk"
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SearchSerializer(paginated_queryset, many=True)
        paginated_response = self.get_paginated_response(serializer.data)

        return Response(data=({'data': paginated_response.data}), template_name='list_item_page.html', status=status.HTTP_200_OK)
