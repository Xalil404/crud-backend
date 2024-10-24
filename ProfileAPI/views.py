from django.shortcuts import render


from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

# Create or retrieve a profile
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
