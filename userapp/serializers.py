from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
from .utils import generate_qr_code

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(cls, attrs):
        data = super().validate(attrs)
        user = cls.user

        # Add custom fields to the token response if needed
        data.update({
            # 'username': user.username,
            # 'password': user.password,
            # Add other fields as needed
        })
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'username', 'email', ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = validated_data.pop('user')
        profile = Profile.objects.create(user=user, **validated_data)
        qr_code_image = generate_qr_code(profile)
        profile.qr_code.save(f'{profile.user.username}_qr.png', qr_code_image)
        return profile


# class ProfileSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = Profile
#         fields = '__all__'
