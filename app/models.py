from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to='blog_images/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )
    posted = models.DateTimeField(default=datetime.now, verbose_name="Дата публикации")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blogpost', kwargs={'pk': self.id})


class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    image = models.ImageField(
        upload_to='tours/images/',  # Папка для сохранения
        verbose_name="Изображение тура",
        blank=True, 
        null=True)
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")
    departure_date = models.DateField(verbose_name="Дата отправления")
    return_date = models.DateField(verbose_name="Дата возвращения")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активный тур")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tour_detail', args=[str(self.id)])


class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    persons = models.PositiveIntegerField(default=1, verbose_name="Количество человек")
    notes = models.TextField(blank=True, verbose_name="Дополнительные пожелания")
    confirmed = models.BooleanField(default=False, verbose_name="Подтверждено")
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Бронирование #{self.id} - {self.tour.title}"

class Comment(models.Model):
    tour = models.ForeignKey(
        'Tour', 
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Тур"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )
    active = models.BooleanField(default=True, verbose_name="Активный")

    class Meta:
        ordering = ('-created_date',)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'Комментарий {self.author} к туру {self.tour}'

# Регистрация модели в админке
admin.site.register(Tour)