from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework import status, renderers
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Count, Q
from relations.serializers import RelationSerializer
from relations.models import Relation
from products.serializers import SearchSerializer
from products.models import MainModel


class UserRelationViewSet(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'item'
    filterset_fields = ['in_liked']
    authentication_classes = [SessionAuthentication]

    def get(self, request, pk):
        return render(request, '404.html', status=404)

    def get_object(self):
        obj, _ = Relation.objects.get_or_create(
            user=self.request.user, item_id=self.kwargs['item'])
        return obj


class AdToFavAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def post(self, request, pk, **kwargs):
        """ Додає товар до улюбленого чи видаляє з нього якщо товар вже був доданий

        Args:
            request (_type_): запит
            pk (_type_): id користувача

        Returns:
            redirect: login  ( якщо користувач не залогінен )
            Response: True - Додано до бажаного, False - видалено з бажаного
        """

        if request.user.is_authenticated:
            item = get_object_or_404(MainModel, pk=pk)
            if item.in_liked.filter(pk=request.user.id).exists():
                item.in_liked.remove(request.user)
                return Response(data={'data': False, 'id': pk}, status=status.HTTP_202_ACCEPTED)
            else:
                item.in_liked.add(request.user)
                return Response(data={'data': True, 'id': pk}, status=status.HTTP_202_ACCEPTED)

        return redirect('login')


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
    queryset = MainModel.objects.filter(is_published=True).annotate(price_w_dis=F('price')-F('price') /
                                                                    100*F('discount'), views=Count('viewed', filter=Q(rati__rate__in=(1, 2, 3, 4, 5)))).order_by('-date_created')
    serializer_class = SearchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'brand']
    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def list(self, request):
        queryset = self.get_queryset()
        query = self.request.query_params.get('search')
        if query:
            data = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query))
            serializer = SearchSerializer(data, many=True)
            return Response(data=({'data': serializer.data}), template_name='list_item_page.html', status=status.HTTP_200_OK)
        return redirect('home')
