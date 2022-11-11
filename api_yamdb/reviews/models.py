from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]

current_year = datetime.now().year


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код для получения токена',
        max_length=10,
        blank=True
    )
    password = models.CharField(
        'Пароль для пользователя',
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        'Почта пользователя',
        max_length=254,
        unique=True
    )

    class Meta:
        ordering = ('username',)


class Parameter(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        help_text='Укажите название'
    )
    slug = models.SlugField(
        verbose_name='Часть url адреса',
        max_length=50,
        unique=True,
        help_text='Должен быть уникальным'
    )

    def __str__(self):
        return (self.name)


class Genre(Parameter):
    pass


class Category(Parameter):
    pass


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
        help_text='Дайте название произведению'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    year = models.IntegerField(
        verbose_name='Год создания произведения',
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(current_year)
        ],
        help_text='Укажите год создания произведению'
    )
    description = models.TextField(
        'описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return (self.name)


class GenreTitle (models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Оцените произведения от 1 до 10',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ]
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="author_review"
            )
        ]
        verbose_name = "Отзыв о произведении"
        verbose_name_plural = "Отзывы о произведении"


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв о произведении",
    )
    text = models.TextField(verbose_name="Ваш комментарий")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзыву"
