from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User, Profile
from cart.models import Order


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserCreateSerializer(UserCreateSerializer):
    username = serializers.CharField()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        return user


class UserLoginSerializer(UserSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserForgotPassSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class ChangePassSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'


class PurchaseHistorySerializer(ModelSerializer):
    email = serializers.EmailField(
        source='customer.email', read_only=True)
    phone_number = serializers.CharField(
        source='customer.phone_number', read_only=True)
    fio = serializers.SerializerMethodField()
    product_image = serializers.ImageField(source='product.main_image')
    product_title = serializers.CharField(source='product.title')
    ordered_date = serializers.DateTimeField(format='%d-%m-%Y', read_only=True)
    summ_product = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_fio(self, obj):
        return f'{obj.customer.last_name} {obj.customer.first_name} {obj.customer.surname}'
    
    def get_summ_product(self, obj):
        return f'{obj.item_price*obj.quantity}'
