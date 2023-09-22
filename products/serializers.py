from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Clothes, Gaming, Relation, Home


class ClothSerializer(ModelSerializer):

    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    in_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Clothes
        fields = ('id', 'title', 'main_image', 'description', 'price', 'discount', 'price_w_dis', 's_code', 'brand',
                  'category', 'rating', 'size', 'season', 'department', 'date_created', 'views', 'in_liked')


class GamingSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    in_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Gaming
        fields = ('id', 'title', 'main_image', 'description', 'price', 'discount', 'price_w_dis', 's_code', 'brand',
                  'category', 'rating', 'material', 'model', 'color', 'date_created', 'views', 'in_liked')


class HomeSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    in_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Home
        fields = ('id', 'title', 'main_image', 'description', 'price', 'discount', 'price_w_dis', 's_code', 'brand',
                  'category', 'rating', 'material', 'color', 'room_type', 'weight', 'dimensions', 'date_created', 'views', 'in_liked')


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
