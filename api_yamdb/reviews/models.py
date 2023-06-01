from django.db import models


class Category(models.Model):
    """Модель для Categories."""
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для Genres."""
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для Titles."""
    name = models.CharField(
        max_length=100
    )
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField()

    class Meta:
        pass

    def __str__(self):
        return self.name
