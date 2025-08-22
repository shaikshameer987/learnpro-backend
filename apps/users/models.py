from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from common.constants import (PROVIDER_CHOICES)


# Create your models here.

# User Manager class contains two functions, one to create user and another to create superuser
# This class will be used by User model to create users and superusers.

class UserManager(BaseUserManager):

    # create a basic user
    def create_user(self, name, email, password=None, **extra_fields):
        if not email or not name:
            raise ValueError("Email, Name are mandatory")
        # to remove trailing whitespaces and covert to lowercase we use normalize_email function.
        email = self.normalize_email(email)

        valid_fields = {f.name for f in self.model._meta.get_fields()}
        filtered_fields = {k: v for k, v in extra_fields.items() if k in valid_fields}

        user = self.model(email=email, name=name, **filtered_fields)

        if(password):
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

# user model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    name = models.CharField(max_length=100, blank=False)
    profile_picture = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    # we dont need to mention email and password as required fields
    # as email mentioned as USERNAME_FIELD and django automatically handles password.

    def __str__(self):
        return self.email


class UserSocialProfile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="social_profiles")
    provider_id = models.CharField(blank=False, null=False)
    provider = models.CharField(choices=PROVIDER_CHOICES, blank=False, max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['provider', 'provider_id'], name='unique_provider_profile')
        ]

    def __str__(self):
        return f"{self.user.email} - {self.provider}"