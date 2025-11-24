from django.db import models
from PIL import Image
import os


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название услуги')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.CharField(max_length=100, blank=True, verbose_name='Цена')
    image = models.ImageField(
        upload_to='services/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Фото услуги',
        help_text='Рекомендуемый размер: 800x600px'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Автоматическое изменение размера изображения при сохранении"""
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            if os.path.exists(img_path):
                img = Image.open(img_path)

                # Максимальные размеры
                max_width = 1200
                max_height = 800

                # Изменяем размер если изображение слишком большое
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    img.save(img_path, optimize=True, quality=85)

class GalleryImage(models.Model):
    title=models.CharField(max_length=200, blank=True)
    image=models.ImageField(upload_to="gallery/")
    uploaded_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'
        # ordering = ['order', 'title']
    def __str__(self): return self.title or self.image.name


class ContactInfo(models.Model):
    phone=models.CharField(max_length=50, blank=True)
    address=models.CharField(max_length=300, blank=True)
    email=models.EmailField(blank=True)
    working_hours=models.CharField(max_length=200, blank=True)
    class Meta:
        verbose_name="Контактная информация"
        verbose_name_plural="Контактная информация"

class Review(models.Model):
    RATING_CHOICES = [
        (5, '5 - Отлично'),
        (4, '4 - Хорошо'),
        (3, '3 - Удовлетворительно'),
        (2, '2 - Плохо'),
        (1, '1 - Очень плохо'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Имя')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name='Оценка')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP-адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_rating_display()}"