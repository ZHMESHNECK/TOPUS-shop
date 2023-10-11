from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Clothes, Gaming, Home


class ClothSerializer(ModelSerializer):

    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)

    class Meta:
        model = Clothes
        # fields = '__all__'
        exclude = ('owner', 'date_created')


class GamingSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)

    class Meta:
        model = Gaming
        # fields = '__all__'
        exclude = ('owner', 'date_created')


class HomeSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)

    class Meta:
        model = Home
        # fields = '__all__'
        exclude = ('owner', 'date_created')
