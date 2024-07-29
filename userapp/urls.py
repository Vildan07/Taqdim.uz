from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('profile/create/', UserProfileCreateAPIView.as_view(), name='profile-create'),
    path('profile/detail/<int:pk>/', UserProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/', UserProfileUpdateDeleteAPIView.as_view(), name='profile-update-delete'),
]