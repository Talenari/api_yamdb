from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


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
        choices=settings.USER_ROLE_CHOICES,
        default=settings.USER
    )
    confirmation_code = models.TextField()

    @property
    def is_admin(self):
        return self.role == settings.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR
