import jwt
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import AppleAuthSerializer

from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def apple_auth(request):
    print("Received data:", request.data)

    serializer = AppleAuthSerializer(data=request.data)
    if serializer.is_valid():
        apple_token = serializer.validated_data['apple_token']
        print("Apple token received:", apple_token)  # Debugging line

        if '.' not in apple_token:
            return JsonResponse({'error': 'Invalid token format'}, status=400)
        
        try:
            apple_public_keys_url = "https://appleid.apple.com/auth/keys"
            apple_public_keys = requests.get(apple_public_keys_url).json()
            print("Apple public keys:", apple_public_keys)  # Debugging line

            decoded_token = decode_apple_token(apple_token, apple_public_keys)
            print("Decoded token:", decoded_token)  # Debugging line

            email = decoded_token.get('email')
            user_id = decoded_token.get('sub')

            return JsonResponse({'message': 'Sign-in successful', 'email': email, 'user_id': user_id})
        
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

