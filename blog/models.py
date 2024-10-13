from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# Модель базы данных Категория
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')

    def __str__(self):
        return self.title

    # Умная ссылка
    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Модель базы данных Статьи
class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Описание статьи')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    video = models.CharField(max_length=500, verbose_name='Ссылка на видео', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# Моделька комментариев
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


# Моделька Профиля

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', verbose_name='Фото профиля', null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_photo(self):
        try:
            return self.photo.url
        except:
            return 'https://bootdey.com/img/Content/avatar/avatar7.png'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
