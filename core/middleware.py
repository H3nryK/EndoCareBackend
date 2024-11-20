from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from .firebase import verify_firebase_token

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        firebase_token = request.headers.get('Firebase-Token')
        if not firebase_token:
            return None

        decoded_token = verify_firebase_token(firebase_token)
        if not decoded_token:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')

        try:
            user = User.objects.get(firebase_uid=decoded_token['uid'])
            return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')