from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import subprocess
import hmac
import hashlib
import json
import os
from .models import Service, GalleryImage, Review

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        service_type = request.POST.get('service_type', 'unlock')

        if name and phone:
            # Отправка email
            subject = f'Новая заявка: {service_type}'
            message = f'''
            Новая заявка с сайта Master Zamok:

            Имя: {name}
            Телефон: {phone}
            Услуга: {service_type}
            Дата: {request.POST.get("form_date", "Не указана")}
            '''

            try:
                send_mail(
                    subject,
                    message,
                    'schkurko.egor@yandex.ru',
                    ['schkurko.egor@yandex.ru'],  # Замените на ваш email
                    fail_silently=False,
                )
                messages.success(request, '✅ Заявка отправлена! Мы вам перезвоним.')
            except Exception as e:
                messages.error(request, f'❌ Ошибка отправки {e}. Позвоните нам: +7 123 456-76-90')
        else:
            messages.error(request, '❌ Заполните все обязательные поля.')

        return redirect('/#order-form')

    return render(request, 'index.html')


# def services(request):
#     if request.method == 'POST':
#         name = request.POST.get('name', '').strip()
#         phone = request.POST.get('phone', '').strip()
#         service_type = request.POST.get('service_type', 'unlock')
#
#         if name and phone:
#             # Отправка email
#             subject = f'Новая заявка: {service_type}'
#             message = f'''
#             Новая заявка с сайта Master Zamok:
#
#             Имя: {name}
#             Телефон: {phone}
#             Услуга: {service_type}
#             Страница: Услуги
#             Дата: {request.POST.get("form_date", "Не указана")}
#             '''
#
#             try:
#                 send_mail(
#                     subject,
#                     message,
#                     'noreply@master-zamok.ru',
#                     ['your-email@yandex.ru'],  # Замените на ваш email
#                     fail_silently=False,
#                 )
#                 messages.success(request, '✅ Заявка отправлена! Мы вам перезвоним.')
#             except Exception as e:
#                 messages.error(request, '❌ Ошибка отправки. Позвоните нам: +7 123 456-76-90')
#         else:
#             messages.error(request, '❌ Заполните все обязательные поля.')
#
#         return redirect('/services/#order-form')
#
#     return render(request, 'services.html')

def services(request):
    services_list = Service.objects.filter()  # Только активные
    context = {
        'services': services_list,
    }
    return render(request, 'services.html', context)

def gallery(request):
    gallery_list = GalleryImage.objects.filter()  # Только активные
    context = {
        'gallery': gallery_list,
    }
    # if request.method == 'POST':
    #     name = request.POST.get('name', '').strip()
    #     phone = request.POST.get('phone', '').strip()
    #     service_type = request.POST.get('service_type', 'unlock')
    #
    #     if name and phone:
    #         # Отправка email
    #         subject = f'Новая заявка: {service_type}'
    #         message = f'''
    #         Новая заявка с сайта Master Zamok:
    #
    #         Имя: {name}
    #         Телефон: {phone}
    #         Услуга: {service_type}
    #         Страница: Галерея
    #         Дата: {request.POST.get("form_date", "Не указана")}
    #         '''
    #
    #         try:
    #             send_mail(
    #                 subject,
    #                 message,
    #                 'noreply@master-zamok.ru',
    #                 ['your-email@yandex.ru'],  # Замените на ваш email
    #                 fail_silently=False,
    #             )
    #             messages.success(request, '✅ Заявка отправлена! Мы вам перезвоним.')
    #         except Exception as e:
    #             messages.error(request, '❌ Ошибка отправки. Позвоните нам: +7 123 456-76-90')
    #     else:
    #         messages.error(request, '❌ Заполните все обязательные поля.')
    #
    #     return redirect('/gallery/#order-form')

    return render(request, 'gallery.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        service_type = request.POST.get('service_type', 'unlock')

        print(
            f"DEBUG: Получены данные - Имя: {name}, Телефон: {phone}, Услуга: {service_type}")  # Отладочная информация

        if name and phone:
            # Отправка email
            subject = f'Новая заявка: {service_type}'
            message = f'''
Новая заявка с сайта Master Zamok:

Имя: {name}
Телефон: {phone}
Услуга: {service_type}
Страница: Контакты
Дата: {request.POST.get("form_date", "Не указана")}
'''

            try:
                print("DEBUG: Пытаемся отправить email...")  # Отладочная информация

                send_mail(
                    subject,
                    message,
                    'noreply@master-zamok.ru',  # from_email
                    ['test@example.com'],  # to_email - можно любой email для теста
                    fail_silently=False,
                )
                print("DEBUG: Email отправлен успешно!")  # Отладочная информация
                messages.success(request, '✅ Заявка отправлена! Мы вам перезвоним.')

            except Exception as e:
                error_msg = f'❌ Ошибка отправки: {str(e)}. Позвоните нам: +7 123 456-76-90'
                print(f"DEBUG: Ошибка при отправке: {e}")  # Отладочная информация
                messages.error(request, error_msg)
        else:
            messages.error(request, '❌ Заполните все обязательные поля.')

        return redirect('/contacts/#order-form')

    return render(request, 'contacts.html')


def get_client_ip(request):
    """Получает IP-адрес клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def otziv(request):
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    
    # Значения формы по умолчанию (для сохранения при ошибках)
    form_data = {
        'name': '',
        'text': '',
        'rating': '5',
        'phone': '',
    }
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        text = request.POST.get('text', '').strip()
        rating = request.POST.get('rating', '5')
        phone = request.POST.get('phone', '').strip()
        
        # Сохраняем данные формы для отображения при ошибках
        form_data = {
            'name': name,
            'text': text,
            'rating': rating,
            'phone': phone,
        }
        
        if name and text:
            # Получаем IP-адрес клиента
            ip_address = get_client_ip(request)
            
            # Защита от спама: проверка на дубликаты за последние 5 минут
            five_minutes_ago = timezone.now() - timedelta(minutes=5)
            recent_duplicate = Review.objects.filter(
                ip_address=ip_address,
                text=text,
                created_at__gte=five_minutes_ago
            ).exists()
            
            if recent_duplicate:
                messages.error(request, '❌ Вы уже отправляли этот отзыв недавно. Пожалуйста, подождите несколько минут.')
                context = {
                    'reviews': reviews,
                    'form_data': form_data,
                }
                return render(request, 'otziv.html', context)
            
            # Защита от спама: ограничение количества отзывов с одного IP (3 в час)
            one_hour_ago = timezone.now() - timedelta(hours=1)
            recent_reviews_count = Review.objects.filter(
                ip_address=ip_address,
                created_at__gte=one_hour_ago
            ).count()
            
            if recent_reviews_count >= 3:
                messages.error(request, '❌ Слишком много отзывов за короткое время. Пожалуйста, попробуйте позже.')
                context = {
                    'reviews': reviews,
                    'form_data': form_data,
                }
                return render(request, 'otziv.html', context)
            
            # Проверка на минимальную длину текста (защита от мусора)
            if len(text) < 10:
                messages.error(request, '❌ Текст отзыва слишком короткий. Пожалуйста, напишите более подробный отзыв.')
                context = {
                    'reviews': reviews,
                    'form_data': form_data,
                }
                return render(request, 'otziv.html', context)
            
            review = Review.objects.create(
                name=name,
                text=text,
                rating=int(rating),
                phone=phone,
                ip_address=ip_address,
                is_published=False  # Требуется модерация
            )
            
            # Отправка уведомления на почту о новом отзыве
            try:
                # Формируем URL админки
                admin_url = f"http://{request.get_host()}/admin/mainapp/review/{review.id}/change/"
                
                subject = f'Новый отзыв на сайте Master Zamok от {name}'
                
                # Контекст для шаблона
                context = {
                    'name': name,
                    'phone': phone,
                    'rating': int(rating),
                    'text': text,
                    'created_at': review.created_at,
                    'admin_url': admin_url,
                }
                
                # Рендерим шаблоны
                text_message = render_to_string('review_notification.txt', context)
                html_message = render_to_string('review_notification.html', context)
                
                # Создаем EmailMultiAlternatives с правильными заголовками
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.REVIEW_NOTIFICATION_EMAIL],
                    reply_to=[settings.DEFAULT_FROM_EMAIL],
                )
                
                # Добавляем HTML версию как альтернативу
                email.attach_alternative(html_message, "text/html")
                
                # Отправляем с таймаутом (fail_silently=True чтобы не падать при ошибках)
                email.send(fail_silently=True)
                
            except Exception as e:
                # Логируем ошибку, но не показываем пользователю
                # Отзыв уже сохранен, поэтому не критично если email не отправился
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Ошибка отправки email о новом отзыве: {e}", exc_info=True)
            
            messages.success(request, '✅ Спасибо за ваш отзыв! Он будет опубликован после модерации.')
            return redirect('/otziv/')
        else:
            messages.error(request, '❌ Заполните все обязательные поля.')
    
    context = {
        'reviews': reviews,
        'form_data': form_data,
    }
    return render(request, 'otziv.html', context)


def garant(request):
    return render(request, 'garant.html')


@csrf_exempt
@require_POST
def github_webhook(request):
    """
    Webhook для автоматического обновления кода с GitHub
    """
    # Получаем секретный токен из настроек
    webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET', '')
    
    if not webhook_secret:
        return JsonResponse({'error': 'Webhook secret not configured'}, status=500)
    
    # Проверяем подпись от GitHub
    signature = request.META.get('HTTP_X_HUB_SIGNATURE_256', '')
    if not signature:
        return JsonResponse({'error': 'Missing signature'}, status=401)
    
    # Вычисляем ожидаемую подпись
    body = request.body
    expected_signature = 'sha256=' + hmac.new(
        webhook_secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    
    # Сравниваем подписи безопасным способом
    if not hmac.compare_digest(signature, expected_signature):
        return JsonResponse({'error': 'Invalid signature'}, status=401)
    
    # Проверяем, что это push событие
    try:
        payload = json.loads(body.decode('utf-8'))
        ref = payload.get('ref', '')
        
        # Определяем имя ветки
        if ref == 'refs/heads/main':
            branch = 'main'
        elif ref == 'refs/heads/master':
            branch = 'master'
        else:
            return JsonResponse({'message': f'Not main/master branch ({ref}), ignoring'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Получаем путь к проекту
    project_path = settings.BASE_DIR
    
    try:
        # Выполняем git pull
        result = subprocess.run(
            ['git', 'pull', 'origin', branch],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return JsonResponse({
                'error': 'Git pull failed',
                'stdout': result.stdout,
                'stderr': result.stderr
            }, status=500)
        
        # Применяем миграции (если есть)
        migrate_result = subprocess.run(
            ['python', 'manage.py', 'migrate', '--noinput'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Собираем статические файлы
        collectstatic_result = subprocess.run(
            ['python', 'manage.py', 'collectstatic', '--noinput'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Перезапускаем gunicorn через systemd (если настроен)
        # Или просто отправляем HUP сигнал
        try:
            # Пытаемся найти процесс gunicorn и отправить HUP
            gunicorn_result = subprocess.run(
                ['pkill', '-HUP', 'gunicorn'],
                capture_output=True,
                text=True,
                timeout=10
            )
        except Exception:
            pass  # Игнорируем ошибки перезапуска
        
        return JsonResponse({
            'message': 'Deployment successful',
            'git_output': result.stdout,
            'migrate_output': migrate_result.stdout if migrate_result.returncode == 0 else migrate_result.stderr,
            'collectstatic_output': collectstatic_result.stdout if collectstatic_result.returncode == 0 else collectstatic_result.stderr,
        }, status=200)
        
    except subprocess.TimeoutExpired:
        return JsonResponse({'error': 'Command timeout'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)