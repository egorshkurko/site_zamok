
from django.contrib import admin
from .models import Service, GalleryImage, ContactInfo, Review

from .models import Service
from django.utils.html import format_html


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'order', 'is_active', 'image_preview']
    list_filter = ['is_active']
    list_editable = ['price', 'order', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

    # Поля в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'price')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )

    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        """Превью фото в админке"""
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "—"

    image_preview.short_description = 'Превью фото'

@admin.register(GalleryImage)
class GA(admin.ModelAdmin):
    list_display=("title","image","uploaded_at")



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'ip_address', 'created_at', 'is_published']
    list_filter = ['is_published', 'rating', 'created_at']
    list_editable = ['is_published']
    search_fields = ['name', 'text', 'phone', 'ip_address']
    readonly_fields = ['created_at', 'ip_address']
