from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, renderers
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect, render
from relations.serializers import RelationSerializer
from relations.models import Relation
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
                return Response(data={'data': False}, status=status.HTTP_202_ACCEPTED) 
            else:
                item.in_liked.add(request.user)
                return Response(data={'data': True}, status=status.HTTP_202_ACCEPTED)

        return redirect('login')


def main(request):
    return render(request, 'main_page.html')
