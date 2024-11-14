import jwt
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AppleAuthSerializer

@api_view(['POST'])
def apple_auth(request):
    # Deserialize the incoming data using the serializer
    serializer = AppleAuthSerializer(data=request.data)
    if serializer.is_valid():
        apple_token = serializer.validated_data['apple_token']
        
        # Verify the token with Apple
        try:
            # Apple's public key endpoint (used to decode the ID token)
            apple_public_keys_url = "https://appleid.apple.com/auth/keys"
            apple_public_keys = requests.get(apple_public_keys_url).json()

            # Decode and verify the token
            decoded_token = decode_apple_token(apple_token, apple_public_keys)
            
            # Retrieve user's email and other details from the decoded token
            email = decoded_token.get('email')
            user_id = decoded_token.get('sub')
            
            # Here, you can use the email or user_id to link the user to your database.
            # If the user exists, log them in; if not, create a new user.

            # For now, just return a success message with user info
            return JsonResponse({'message': 'Sign-in successful', 'email': email, 'user_id': user_id})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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

