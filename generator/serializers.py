from.models import User,PasswordEntry
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class PasswordEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordEntry('id','user','service_name','generated_password')
