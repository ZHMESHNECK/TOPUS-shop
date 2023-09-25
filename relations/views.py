from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from relations.serializers import RelationSerializer
from relations.models import Relation
from django.shortcuts import render


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
