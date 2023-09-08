from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Clothes, Gaming, Rating


class ClothSerializer(ModelSerializer):

    rate_count = serializers.DecimalField(
        max_digits=2, decimal_places=1, read_only=True)
    price_w_dis = serializers.IntegerField(read_only=True)

    class Meta:
        model = Clothes
        fields = ('id', 'title', 'price', 'owner',
                  'category', 'rate_count', 'price_w_dis', 'discount')


class GamingSerializer(ModelSerializer):
    class Meta:
        model = Gaming
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('item_id', 'rate')
