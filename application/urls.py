from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from .views import get_vk_token, VkTokenObtainPairView, RefreshTokenView
from application.views import MedicineView, AboutMeView, MedicineTypeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('vk_token/', get_vk_token, name='vk_token_obtain_pair'),
    #path('', TokenRefreshView.as_view(), name='token_refresh'),
]


LIST = {
    'get': 'list',
    'post': 'create'
}

DETAIL = {
    'delete': 'destroy',
    'get': 'retrieve',
    'patch': 'partial_update',
    'put': 'update',
}

urlpatterns += [
    path('medicine/', MedicineView.as_view(LIST)),
    path('medicine/<int:pk>/', MedicineView.as_view(DETAIL)),
    path('current_user/', AboutMeView.as_view()),
    path('medicine_type/', MedicineTypeView.as_view())
]
