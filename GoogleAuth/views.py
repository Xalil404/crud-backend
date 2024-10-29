from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    try:
        # Verify the token with Google's API
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), YOUR_CLIENT_ID)

        # Get user info
        email = idinfo['email']
        name = idinfo['name']

        # Get or create the user
        user, created = User.objects.get_or_create(email=email, defaults={'username': email, 'first_name': name})

        return Response({'message': 'User logged in successfully', 'user': {'email': email, 'name': name}}, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
