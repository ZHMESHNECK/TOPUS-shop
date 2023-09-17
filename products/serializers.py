from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Clothes, Gaming, Rating, Home


class ClothSerializer(ModelSerializer):

    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)

    class Meta:
        model = Clothes
        fields = ('id', 'title', 'description', 'price', 'discount', 'price_w_dis', 's_code', 'brand',
                  'category', 'rating',  'size', 'season', 'department', 'date_created', 'views')


class GamingSerializer(ModelSerializer):
    class Meta:
        model = Gaming
        fields = '__all__'


class HomeSerializer(ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'


class RatingSerializer(ModelSerializer):

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            user=validated_data.get('user', None),
            item=validated_data.get('item', None),
            defaults={'rate': validated_data.get('rate')}
        )
        return rating

    class Meta:
        model = Rating
        fields = ('item_id', 'rate')
