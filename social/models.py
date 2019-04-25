from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

from config.default import SECRET_KEY

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(db_index=True, max_length=255, unique=True)

    phonenumber = models.BooleanField(default=True)

    is_tenant = models.BooleanField(default=True)

    is_landlord = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.email