import jwt
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import AppleAuthSerializer

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
def apple_auth(request):
    print("Received data:", request.data)

    # Validate incoming data with the serializer
    serializer = AppleAuthSerializer(data=request.data)
    if serializer.is_valid():
        apple_token = serializer.validated_data['apple_token']
        print("Apple token received:", apple_token)  # Debugging line

        if '.' not in apple_token:
            return JsonResponse({'error': 'Invalid token format'}, status=400)
        
        try:
            # Fetch Apple's public keys to verify the token
            apple_public_keys_url = "https://appleid.apple.com/auth/keys"
            apple_public_keys = requests.get(apple_public_keys_url).json()
            print("Apple public keys:", apple_public_keys)  # Debugging line

            # Decode and verify the Apple token
            decoded_token = decode_apple_token(apple_token, apple_public_keys)
            print("Decoded token:", decoded_token)  # Debugging line

            # Extract user information from the decoded token
            email = decoded_token.get('email')
            user_id = decoded_token.get('sub')

            # Create or update the user
            user, created = create_or_update_user(email, user_id, decoded_token)
            
            # Generate a token for the user if using token-based authentication
            token, _ = Token.objects.get_or_create(user=user)

            return JsonResponse({
                'message': 'Sign-in successful',
                'email': email,
                'user_id': user_id,
                'token': token.key
            })
        
        except Exception as e:
            print("Error during token verification:", e)  # Debugging line
            return JsonResponse({'error': str(e)}, status=400)

    print("Serializer errors:", serializer.errors)  # Debugging line
    return JsonResponse({'error': 'Invalid data'}, status=400)


def decode_apple_token(token, apple_public_keys):
    # Get the key ID (kid) from the token header
    unverified_header = jwt.get_unverified_header(token)
    
    if unverified_header is None or 'kid' not in unverified_header:
        raise ValueError("Invalid header in Apple token")

    kid = unverified_header['kid']
    
    # Find the matching key from Apple's public keys
    key = next((key for key in apple_public_keys['keys'] if key['kid'] == kid), None)
    if key is None:
        raise ValueError("Public key not found")

    # Decode the token using the public key
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

    # Decode and verify the token with additional checks
    decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], audience=settings.APPLE_CLIENT_ID, options={"verify_exp": True})

    # Check if the issuer is Apple
    if decoded_token.get('iss') != 'https://appleid.apple.com':
        raise ValueError("Invalid issuer")
    
    return decoded_token


def create_or_update_user(email, user_id, decoded_token):
    # Check if the user already exists using either the email or user_id (sub)
    user = User.objects.filter(email=email).first()

    if not user:
        # Create a new user if not found
        user = User.objects.create_user(
            username=email,  # You can use the email or generate a unique username
            email=email,
            password=None  # Apple does not send a password
        )
    
    # Update the user with information from the decoded token
    user.first_name = decoded_token.get('given_name', '')
    user.last_name = decoded_token.get('family_name', '')
    
    # Optionally, store the Apple user ID (sub) in the user model for future reference
    user.profile.apple_user_id = user_id  # Assuming you have a custom user profile model
    user.save()

    return user, False  # Returning user and False to indicate we didn't create the user again
