from rest_framework import serializers
from .models import Birthday

class BirthdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Birthday
        fields = '__all__'
