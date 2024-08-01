from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('profile/create/', UserProfileCreateAPIView.as_view(), name='profile-create'),
    path('profile/<str:username>/detail/', UserProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/', UserProfileUpdateDeleteAPIView.as_view(), name='profile-update-delete'),
]