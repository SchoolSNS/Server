from rest_framework import serializers
from .models import User
from django.contrib import auth
from datetime import datetime, timedelta

class RegisterSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True, allow_null=True)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    introduce = serializers.CharField(required=False)
    
    class Meta :
        model = User
        fields = ['email', 'username', 'password', 'identity', 'school', 'image', 'introduce']
        
    def create (self, validate_data) :
        return User.objects.create_user(**validate_data)

class LoginSerializer (serializers.ModelSerializer) :
    password = serializers.CharField(max_length=255, min_length=8)

    class Meta :
        model = User
        fields = ['email', 'password']

class UserProfileSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True)
    
    class Meta :
        model = User
        fields = ['id', 'email', 'username', 'image', 'identity', 'school']