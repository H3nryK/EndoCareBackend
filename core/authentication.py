from firebase_admin import auth
from rest_framework import authentication
from django.contrib.auth import get_user_model
from rest_framework import exceptions

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        id_token = auth_header.split(' ').pop()
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user, created = User.objects.get_or_create(
                firebase_uid=uid,
                defaults={
                    'username': decoded_token.get('email', uid),
                    'email': decoded_token.get('email', '')
                }
            )
            return (user, None)
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))