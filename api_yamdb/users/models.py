from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import USER_ROLE_CHOICES


class User(AbstractUser):
    email = models.EmailField(
        max_length=150,
        blank=False,
        null=False,
        unique=True
    )
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
        default='user'
    )
