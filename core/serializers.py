from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firebase_uid', 'phone_number', 
                 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['firebase_uid', 'created_at', 'updated_at']