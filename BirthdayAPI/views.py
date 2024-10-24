from django.shortcuts import render
from rest_framework import generics
from .models import Birthday
from .serializers import BirthdaySerializer
from rest_framework.permissions import IsAuthenticated

class BirthdayListCreateView(generics.ListCreateAPIView):
    serializer_class = BirthdaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the birthdays for the logged-in user
        return Birthday.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user to the logged-in user when creating a birthday
        serializer.save(user=self.request.user)


class BirthdayDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BirthdaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the birthdays for the logged-in user
        return Birthday.objects.filter(user=self.request.user)
