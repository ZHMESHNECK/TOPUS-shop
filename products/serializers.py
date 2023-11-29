from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Clothes, Gaming, Home, MainModel


class ClothSerializer(ModelSerializer):

    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Clothes
        # fields = '__all__'
        exclude = ('owner', 'viewed', 'is_published', 'category')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class GamingSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Gaming
        # fields = '__all__'
        exclude = ('owner', 'viewed', 'is_published', 'category')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class HomeSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Home
        # fields = '__all__'
        exclude = ('owner', 'viewed', 'is_published', 'category')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class SearchSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = MainModel
        # fields = '__all__'
        exclude = ('owner', 'viewed', 'is_published', 'category')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
