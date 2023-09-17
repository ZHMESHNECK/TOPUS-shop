from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from users.models import User
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model


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
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'
