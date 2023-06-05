from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import CHOICES


class User(AbstractUser):
    email = models.EmailField(max_length=150, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=CHOICES,
        default='user'
    )
