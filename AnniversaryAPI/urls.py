from django.urls import path
from .views import AnniversaryListCreateView, AnniversaryDetailView

urlpatterns = [
    path('anniversaries/', AnniversaryListCreateView.as_view(), name='anniversary-list-create'),
    path('anniversaries/<int:pk>/', AnniversaryDetailView.as_view(), name='anniversary-detail'),
]
