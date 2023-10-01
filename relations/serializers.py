from rest_framework.serializers import ModelSerializer
from relations.models import Relation


class RelationSerializer(ModelSerializer):

    def create(self, validated_data):
        relation = Relation.objects.update_or_create(
            user=validated_data.get('user', None),
            item=validated_data.get('item', None),
            defaults={'rate': validated_data.get(
                'rate'), 'comment': validated_data.get('comment'), 'parent': validated_data.get('parent'), 'in_liked': validated_data.get('in_liked')}
        )
        return relation

    class Meta:
        model = Relation
        fields = ('item_id', 'rate', 'comment', 'parent', 'in_liked')
