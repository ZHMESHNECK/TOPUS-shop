from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Clothes, Gaming, Home, MainModel


class BaseItemSerializer(ModelSerializer):
    price_w_dis = serializers.DecimalField(
        max_digits=7, decimal_places=2, read_only=True)
    views = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        exclude = ('owner', 'viewed', 'is_published')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_main_image(self, obj):
        return obj.main_image.url


class ClothSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Clothes


class GamingSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Gaming


class HomeSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = Home


class SearchSerializer(BaseItemSerializer):
    class Meta(BaseItemSerializer.Meta):
        model = MainModel
