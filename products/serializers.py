from rest_framework.serializers import ModelSerializer
from products.models import Clothes, Gaming

class ClosthSerializer(ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'


class GamingSerializer(ModelSerializer):
    class Meta:
        model = Gaming
        fields = '__all__'