from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from .constants import Provider
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):
    """ Custom user model manager for authentication """

    def create_user(self, email, password, provider, sub=None, **extra_fields):
        """ Create and save a User with the given email and password """

        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        if sub:
            user = self.model(email=email, provider=provider, sub=sub, **extra_fields)
        else:
            user = self.model(email=email, provider=provider, **extra_fields)

        user.set_password(password)
        if provider != "wejpal-user":
            user.is_active = True
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Method to  a SuperUser with the given email and password """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('provider', "wejpal-user")

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model for all authentication process """

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    provider = models.CharField(max_length=20, choices=Provider.choices)
    sub = models.CharField(max_length=1000, unique=True, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)
