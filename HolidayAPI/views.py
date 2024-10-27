from django.shortcuts import render
from rest_framework import generics
from .models import Holiday
from .serializers import HolidaySerializer
from rest_framework.permissions import IsAuthenticated



class HolidayListCreateView(generics.ListCreateAPIView):
    serializer_class = HolidaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the birthdays for the logged-in user
        return Holiday.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user to the logged-in user when creating a birthday
        serializer.save(user=self.request.user)


class HolidayDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HolidaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the birthdays for the logged-in user
        return Holiday.objects.filter(user=self.request.user)