from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250, required=True)
    password = serializers.CharField(max_length=250, required=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('The username or password is wrong.')
        self.instance = user
        return data
