from rest_framework import serializers
from .models import User
from django.contrib import auth
from datetime import datetime, timedelta

class RegisterSerializer (serializers.ModelSerializer) :
    profile = serializers.ImageField(use_url=True, allow_null=True)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    
    class Meta :
        model = User
        fields = ['email', 'username', 'password', 'identity', 'school', 'profile', 'introduce']
        
    def create (self, validate_data) :
        return User.objects.create_user(**validate_data)

class LoginSerializer (serializers.ModelSerializer) :
    password = serializers.CharField(max_length=255, min_length=8)

    class Meta :
        model = User
        fields = ['email', 'password']

class UserProfileSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    
    class Meta :
        model = User
        fields = ['id', 'email', 'username', 'image', 'following', 'followers']

    def get_following (self, obj) :
        serializer = FollowingSerializer(obj.following.all(), many=True).data
        return len(serializer)

    def get_followers (self, obj) :
        serializer = FollowersSerializer(obj.followers.all(), many=True).data
        return len(serializer)