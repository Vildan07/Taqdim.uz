from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model, authenticate

from .serializers import *
from .models import Profile
from .permissions import IsOwnerOrReadOnly
from .utils import generate_qr_code

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
#
#
# class UserProfileDetailAPIView(generics.RetrieveAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = (AllowAny,)
#
#     def get_object(self):
#         username = self.kwargs.get('username'.lower())
#         profile = Profile.objects.get(username=username)
#         return profile


class UserProfileUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'username'

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        username = self.kwargs.get('username'.lower())
        profile = get_object_or_404(Profile, username=username)
        return profile

# class ProfileView(APIView):
#     def get(self, request, *args, **kwargs):
#         profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ProfileDetailView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, username, *args, **kwargs):
#         profile = get_object_or_404(Profile, username=username)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class ProfileUpdateView(APIView):
#     def put(self, request, *args, **kwargs):
#         profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
