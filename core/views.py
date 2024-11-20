from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .firebase import verify_firebase_token

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def register(self, request):
        firebase_token = request.headers.get('Firebase-Token')
        if not firebase_token:
            return Response(
                {'error': 'Firebase token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        decoded_token = verify_firebase_token(firebase_token)
        if not decoded_token:
            return Response(
                {'error': 'Invalid Firebase token'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        firebase_uid = decoded_token['uid']
        email = decoded_token.get('email')

        # Create or update user
        user, created = User.objects.get_or_create(
            firebase_uid=firebase_uid,
            defaults={
                'email': email,
                'username': email  # You might want to modify this
            }
        )

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
