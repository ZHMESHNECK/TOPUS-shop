from rest_framework.serializers import ModelSerializer
from relations.models import Relation

class RelationSerializer(ModelSerializer):

    def create(self, validated_data):
        rating = Relation.objects.update_or_create(
            user=validated_data.get('user', None),
            item=validated_data.get('item', None),
            defaults={'rate': validated_data.get('rate')}
        )
        return rating

    class Meta:
        model = Relation
        fields = ('item_id', 'rate','in_liked')