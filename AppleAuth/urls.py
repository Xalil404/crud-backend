# urls.py

from django.urls import path
from .views import apple_auth

urlpatterns = [
    path('api/auth/apple/mobile/', apple_auth, name='apple-auth'),
]
