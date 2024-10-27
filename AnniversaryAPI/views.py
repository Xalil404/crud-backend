from django.shortcuts import render
from rest_framework import generics
from .models import Anniversary
from .serializers import AnniversarySerializer
from rest_framework.permissions import IsAuthenticated


class AnniversaryListCreateView(generics.ListCreateAPIView):
    serializer_class = AnniversarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the birthdays for the logged-in user
        return Anniversary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user to the logged-in user when creating a birthday
        serializer.save(user=self.request.user)


class AnniversaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnniversarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the birthdays for the logged-in user
        return Anniversary.objects.filter(user=self.request.user)