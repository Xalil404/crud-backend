from django.urls import path
from .views import BirthdayListCreateView, BirthdayDetailView

urlpatterns = [
    path('birthdays/', BirthdayListCreateView.as_view(), name='birthday-list-create'),
    path('birthdays/<int:pk>/', BirthdayDetailView.as_view(), name='birthday-detail'),
]
