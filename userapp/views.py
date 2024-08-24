import re

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from .models import Profile
from .permissions import IsOwnerOrReadOnly
from .utils import *

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileCreateSerializer

    def perform_create(self, serializer):
        profile = serializer.save(user=self.request.user)
        qr_code_image = generate_qr_code(profile)
        profile.qr_code.save(f'{profile.user.username}_qr.png', qr_code_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        username = self.kwargs.get('username'.lower())
        profile = get_object_or_404(Profile, username=username)
        return profile


class UserProfileUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'username'

    def get_object(self):
        username = self.kwargs.get('username').lower()
        profile = get_object_or_404(Profile, username=username)

        # Проверяем права доступа на уровне объекта
        self.check_object_permissions(self.request, profile)

        return profile

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        profiles = Profile.objects.filter(user=user)
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class SocialMediaIconView(APIView):
    def get(self, request, format=None):
        url = request.query_params.get('url')
        id = request.query_params.get('id')

        if url:
            icons = SocialMediaIcon.objects.all()

            for icon in icons:
                if re.match(icon.url_pattern, url):
                    serializer = SocialMediaIconSerializer(icon)
                    return Response(serializer.data)

            return Response({'error': 'Иконка не найдена'}, status=status.HTTP_404_NOT_FOUND)
        elif id:
            icon = get_object_or_404(SocialMediaIcon, pk=id)
            serializer = SocialMediaIconSerializer(icon)
            return Response(serializer.data)

        else:
            return Response({'error': 'Необходимо указать URL'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        try:
            user = User.objects.get(username=username)
            code = PasswordResetCode.objects.create(
                user=user,
                code=generate_code()
            )
            # Send email with the reset code
            send_mail(
                'Password Reset Code',
                f'Your password reset code is {code.code}',
                settings.DEFAULT_FROM_EMAIL,
                [username],
                fail_silently=False,
            )
            return Response({'message': 'Password reset code sent'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_password_reset(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']
        try:
            reset_code = PasswordResetCode.objects.get(code=code)
            user = reset_code.user
            user.password = make_password(new_password)
            user.save()
            reset_code.delete()  # Delete the used reset code
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        except PasswordResetCode.DoesNotExist:
            return Response({'error': 'Invalid reset code'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
