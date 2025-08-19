import re
from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth import authenticate
from common.constants import (PROVIDER_CHOICES, CREDENTIALS)


class RegisterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=10)
    provider = serializers.ChoiceField(choices=PROVIDER_CHOICES)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        email = data.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User already exists with this email."})

        return data

    def create(self, validated_data):
        return User.objects.create_user(
            name=validated_data.get('name'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            provider=validated_data.get('provider'),
            is_staff=validated_data.get('is_staff', False),
            is_superuser=validated_data.get('is_superuser', False),
        )

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    provider = serializers.ChoiceField(choices=PROVIDER_CHOICES)

    def validate(self, attrs):
        email    = attrs.get("email")
        password = attrs.get("password")
        provider = attrs.get("provider")

        if not email or not provider:
            raise serializers.ValidationError({"email" : "Email and Provider are required"})

        if provider == CREDENTIALS:
            if not password:
                raise serializers.ValidationError({"password": "Password is required"})

            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError({"email": "User does not exist with this email or password"})

        else:
            user = User.objects.filter(email=email, provider=provider).first()
            if not user:
                raise serializers.ValidationError({"email": "User does not exist with this email or password"})

        attrs["user"] = user
        return attrs

    def to_representation(self, instance):
        user = instance.get("user")
        return RegisterUserSerializer(user).data
