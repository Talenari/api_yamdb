from django.db import models


class Category(models.Model):
    """Модель для Categories."""
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        max_length=50, unique=True
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для Genres."""
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        max_length=50, unique=True
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


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
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        Genre
    )

    class Meta:
        pass

    def __str__(self):
        return self.name
