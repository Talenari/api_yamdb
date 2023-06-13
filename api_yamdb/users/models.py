from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        verbose_name='электронная почта'
    )
    bio = models.TextField(blank=True, null=True, verbose_name='биография')
    role = models.CharField(
        max_length=10,
        choices=settings.USER_ROLE_CHOICES,
        default=settings.USER,
        verbose_name='роль'
    )
    confirmation_code = models.TextField(verbose_name='код подтверждения')

    @property
    def is_admin(self):
        return self.role == settings.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR
