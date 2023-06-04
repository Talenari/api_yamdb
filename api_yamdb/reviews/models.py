from django.db import models

from reviews.constants import STRING_LENGTH


class Category(models.Model):
    """Модель для Categories."""
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        max_length=50, unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:STRING_LENGTH]


class Genre(models.Model):
    """Модель для Genres."""
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        max_length=50, unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:STRING_LENGTH]


class Title(models.Model):
    """Модель для Titles."""
    name = models.CharField(
        max_length=256
    )
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='title'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:STRING_LENGTH]
