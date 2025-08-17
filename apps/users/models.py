from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

# User Manager class contains two functions, one to create user and another to create superuser
# This class will be used by User model to create users and superusers.

class UserManager(BaseUserManager):

    # create a basic user
    def create_user(self, name, email, password, is_staff, is_superuser, **extra_fields):
        if not email or not password or not name:
            raise ValueError("Email, Name and Password are mandatory")
        # to remove trailing whitespaces and covert to lowercase we use normalize_email function.
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user

# user model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    name = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    # we dont need to mention email and password as required fields
    # as email mentioned as USERNAME_FIELD and django automatically handles password.

    def __str__(self):
        return self.email