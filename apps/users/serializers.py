import re
from rest_framework import serializers
from apps.users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=10)
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
            is_staff=validated_data.get('is_staff', False),
            is_superuser=validated_data.get('is_superuser', False),
        )
