from rest_framework import serializers
from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["email", "phone_number", "username", "address", "password"]


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["email", "phone_number", "username", "address", "password"]