from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from django.conf import settings

User = get_user_model()


class Category(models.Model):
    """Модель для Categories."""
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.STRING_LENGTH]


class Genre(models.Model):
    """Модель для Genres."""
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.STRING_LENGTH]


class Title(models.Model):
    """Модель для Titles."""
    name = models.CharField(
        max_length=256
    )
    year = models.PositiveSmallIntegerField(db_index=True)
    description = models.TextField(
        'Описание', blank=True, null=True
    )
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
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.STRING_LENGTH]


class Review(models.Model):
    """Модель для Reviews."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
    )
    text = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(settings.MIN_SCR),
                    MaxValueValidator(settings.MAX_SCR)],
        error_messages={'validators': 'Оценка от 1 до 10'},
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]

    def __str__(self):
        return self.text[:settings.STRING_LENGTH]


class Comment(models.Model):
    """Модель для Comments."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.CharField('текст комментария', max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:settings.STRING_LENGTH]
