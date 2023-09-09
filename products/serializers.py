from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Clothes, Gaming, Rating, Home
from django.contrib.auth.models import User


class ClothSerializer(ModelSerializer):

    price_w_dis = serializers.IntegerField(read_only=True)
    views = serializers.CharField(read_only=True)

    class Meta:
        model = Clothes
        fields = ('id', 'title', 'description', 'price', 'discount', 'brand',
                  'category', 'rating', 'price_w_dis', 'date_created', 'views')


class GamingSerializer(ModelSerializer):
    class Meta:
        model = Gaming
        fields = '__all__'


class HomeSerializer(ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('item_id', 'rate')
