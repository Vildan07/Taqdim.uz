from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from .serializers import *
from .models import Profile
from .permissions import IsOwnerOrReadOnly
from .utils import generate_qr_code

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
    serializer_class = UserProfileCreateSerializer

    def perform_create(self, serializer):
        profile = serializer.save(user=self.request.user)
        qr_code_image = generate_qr_code(profile)
        profile.qr_code.save(f'{profile.user.username}_qr.png', qr_code_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        profile = Profile.objects.get(user=user)
        return profile


class UserProfileUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

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
