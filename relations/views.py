from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from relations.serializers import RelationSerializer
from relations.models import Relation


class UserRelationViewSet(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'item'
    filterset_fields = ['in_liked']
    authentication_classes = [SessionAuthentication]

    def get(self, request, pk):
        return render(request, 'products/templates/404.html', status=404)

    def get_object(self):
        obj, _ = Relation.objects.get_or_create(
            user=self.request.user, item_id=self.kwargs['item'])
        return obj


def main(request):
    return render(request, 'main_page.html')
