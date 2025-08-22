from rest_framework import serializers
from apps.users.models import (User, UserSocialProfile)
from django.contrib.auth import authenticate
from common.constants import (PROVIDER_CHOICES, CREDENTIALS)
from urllib.request import urlopen
from django.core.files.base import ContentFile
from utils.helpers import upload_to_s3
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "last_login"]

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True)
    provider = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=False, write_only=True, min_length=10)
    providerId = serializers.CharField(required=False, allow_blank=True, write_only=True)
    profilePicture = serializers.CharField(required=False)

    def validate(self, data):
        provider = data.get("provider")
        password = data.get("password")
        provider_id = data.get("providerId")

        if provider == CREDENTIALS:
            if not password:
                raise serializers.ValidationError({"password": "Password is required for credentials signup."})

        else:
            if not provider_id:
                raise serializers.ValidationError({"provider": "Provider Id required for social signup"})

        return data

    def create(self, validated_data):
        email = validated_data.get("email")
        provider = validated_data.get("provider")
        provider_id = validated_data.get("providerId")
        is_staff = validated_data.get("isStaff", False)
        is_superuser = validated_data.get("isSuperuser", False)
        profile_picture = validated_data.get("profilePicture", None)

        s3_url = None
        if profile_picture:
            try:
                response = urlopen(profile_picture)
                print(response.getcode() == 200)
                if response.getcode() == 200:
                    image_content = ContentFile(response.read())
                    s3_url = upload_to_s3(image_content, f"dp/{email}.jpg")
            except Exception as e:
                pass

        with transaction.atomic():
            user = User.objects.filter(email=email).first()

            if not user:
                user = User.objects.create_user(is_staff=is_staff, is_superuser=is_superuser, profile_picture=s3_url, **validated_data)

            if provider != CREDENTIALS:
                profile_exists = UserSocialProfile.objects.filter(user=user,provider=provider,provider_id=provider_id).exists()

                if not profile_exists:
                    UserSocialProfile.objects.create(provider=provider, user=user, provider_id=provider_id)

        return user
