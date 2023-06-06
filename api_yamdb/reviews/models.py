from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

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


class Reviews(models.Model):
    """Модель для Reviews."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        error_messages={'validators': 'Оценка от 1 до 10'},
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Модель для Comments."""
    review = models.ForeignKey(
        Reviews,
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
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
