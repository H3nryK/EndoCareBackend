from rest_framework import serializers
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['next_period', 'cycle_length', 'last_period', 
                 'tracked_cycles', 'logged_symptoms']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_picture', 
                 'profile', 'firebase_uid']
        read_only_fields = ['firebase_uid']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        # Update user data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profile data
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance