from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import firebase_admin
from firebase_admin import auth
from .models import *

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        id_token = auth_header.split(' ').pop()
        try:
            decoded_token = auth.verify_id_token(id_token)
            firebase_uid = decoded_token['uid']
            
            try:
                user = User.objects.get(firebase_uid=firebase_uid)
                return (user, None)
            except User.DoesNotExist:
                # Create new user if they don't exist
                email = decoded_token.get('email', '')
                name = decoded_token.get('name', '').split()
                first_name = name[0] if name else ''
                last_name = name[-1] if len(name) > 1 else ''
                
                user = User.objects.create(
                    firebase_uid=firebase_uid,
                    email=email,
                    username=email,  # Using email as username
                    first_name=first_name,
                    last_name=last_name,
                    profile_picture=decoded_token.get('picture', '')
                )
                UserProfile.objects.create(user=user)
                return (user, None)
                
        except Exception as e:
            raise AuthenticationFailed(str(e))