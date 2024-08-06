from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('profile/create/', UserProfileCreateAPIView.as_view(), name='profile-create'),
    path('profile/detail/', UserProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/', UserProfileUpdateDeleteAPIView.as_view(), name='profile-update-delete'),
]