from rest_framework import serializers

class SchoolSearchSerializer (serializers.Serializer) :
    school = serializers.CharField()