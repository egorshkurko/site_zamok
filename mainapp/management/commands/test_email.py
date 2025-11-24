from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Тестирует отправку email о новом отзыве'

    def handle(self, *args, **options):
        self.stdout.write('Тестирование отправки email...')
        
        # Тестовые данные
        context = {
            'name': 'Тестовый пользователь',
            'phone': '+7 (999) 123-45-67',
            'rating': 5,
            'text': 'Это тестовый отзыв для проверки отправки email.',
            'created_at': '2024-11-24 20:00:00',
            'admin_url': 'http://masterzamok.pro/admin/mainapp/review/1/change/',
        }
        
        try:
            # Рендерим шаблоны
            text_message = render_to_string('review_notification.txt', context)
            html_message = render_to_string('review_notification.html', context)
            
            # Проверяем настройки
            self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
            self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
            self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
            self.stdout.write(f'FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
            self.stdout.write(f'TO_EMAIL: {settings.REVIEW_NOTIFICATION_EMAIL}')
            
            # Создаем email
            email = EmailMultiAlternatives(
                subject='Тестовое письмо: Новый отзыв на сайте Master Zamok',
                body=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.REVIEW_NOTIFICATION_EMAIL],
                reply_to=[settings.DEFAULT_FROM_EMAIL],
            )
            
            email.attach_alternative(html_message, "text/html")
            
            # Отправляем
            result = email.send(fail_silently=False)
            
            self.stdout.write(self.style.SUCCESS(f'✅ Email отправлен успешно! Результат: {result}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка отправки email: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

