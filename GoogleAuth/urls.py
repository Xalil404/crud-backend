from django.urls import path
from .views import google_login

urlpatterns = [
    path('api/auth/google/', google_login, name='google_login'),  # Use the function-based view
]
