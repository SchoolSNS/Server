from rest_framework import serializers
from .models import DeviceToken, Description
from feedAPI.serializers import PostSerializer

class DeviceTokenSerializer (serializers.ModelSerializer) :

    class Meta :
        model = DeviceToken
        fields = ('device_token', )

    def create (self, validate_data) :
        return DeviceToken.objects.create(**validate_data)

class DescriptionSerializer (serializers.ModelSerializer) :
    post = PostSerializer(read_only=True)
    
    class Meta :
        model = Description
        fields = ('post', 'title')