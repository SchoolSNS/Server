from rest_framework import serializers
from .models import User
from django.contrib import auth
from django.conf import settings
import requests

class RegisterSerializer (serializers.ModelSerializer) :
    image = serializers.ImageField(use_url=True, allow_null=True)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    introduce = serializers.CharField(required=False, allow_null=True)
    
    class Meta :
        model = User
        fields = ['email', 'username', 'password', 'identity', 'school', 'image', 'introduce']
        
    def create (self, validate_data) :
        return User.objects.create_user(**validate_data)

    def validate (self, attrs) :  
        school = attrs.get('school', '')

        error = {}

        url = 'https://open.neis.go.kr/hub/schoolInfo'
        param = {'key': settings.SCHOOL_API_KEY, 'Type': 'json', 'pIndex': 1, 'pSize': 100, 'SCHUL_NM': school}

        res = requests.get(url, params=param)

        if res.json().get('RESULT', None) is not None :
            if res.json().get('RESULT', None).get('MESSAGE', None) is not None :
                error['message'] = '학교 이름을 확인해주세요.'
                raise serializers.ValidationError(error)

        return attrs

        
class LoginSerializer (serializers.ModelSerializer) :
    password = serializers.CharField(max_length=255, min_length=8)

    class Meta :
        model = User
        fields = ['email', 'password']

class ChangeProfileSerializer (serializers.ModelSerializer) :

    class Meta :
        model = User
        fields = ('image', 'introduce')

    def update (self, instance, validate_data) :
        image = validate_data.get('image', None)
        introduce = validate_data.get('introduce', None)

        instance.image = image
        instance.introduce = introduce

        instance.save(update_fields=('image', 'introduce'))

        return instance

class UserProfileSerializer (serializers.ModelSerializer) :
    profile = serializers.ImageField(source='image')

    class Meta :
        model = User
        fields = ['id', 'email', 'username', 'profile', 'identity', 'introduce', 'school']