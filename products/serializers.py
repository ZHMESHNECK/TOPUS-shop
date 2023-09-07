from rest_framework.serializers import ModelSerializer
from products.models import Clothes, Gaming, Rating


class ClosthSerializer(ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'


class GamingSerializer(ModelSerializer):
    class Meta:
        model = Gaming
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('Clothes_id', 'Gaming_id', 'rate')
