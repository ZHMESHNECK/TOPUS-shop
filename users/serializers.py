from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User, Profile


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
    class Meta(UserCreateSerializer.Meta):
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
