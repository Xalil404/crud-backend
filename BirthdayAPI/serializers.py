# birthdays/serializers.py
from rest_framework import serializers
from .models import Birthday

class BirthdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Birthday
        fields = ['id', 'user', 'description', 'date']  # Include 'user' in the fields

    def create(self, validated_data):
        # Automatically set the user to the currently authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)