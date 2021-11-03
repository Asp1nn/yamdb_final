from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import year_not_from_the_future

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')
]


class User(AbstractUser):
    bio = models.TextField(
        'biografy',
        blank=True
    )
    email = models.EmailField(
        'email address',
        unique=True
    )
    role = models.CharField(
        "user's role",
        choices=ROLES,
        default=USER,
        max_length=50
    )
    REQUIRED_FIELDS = ['email']


class Genre(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name_plural = "Жанры"
        verbose_name = 'Жанр'
        ordering = ['-pk']

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название категории'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='год выпуска',
        validators=[year_not_from_the_future],

    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория'
    )

    def __str__(self):
        return (
            f'{self.author.username}, {self.name} {self.description}, '
            f'{self.year}, {self.rating}, {self.category}'
        )


class Review(models.Model):
    RATE_CHOICE = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Ревьюер',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        choices=RATE_CHOICE

    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return (
            f'{self.author.username}, {self.pub_date},'
            f' {self.title}, {self.text[:15]}'
        )

    class Meta:
        verbose_name = 'Oтзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Комментатор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Tекст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return (
            f'{self.author.username}, {self.pub_date},'
            f' {self.review}, {self.text[:15]}'
        )

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
