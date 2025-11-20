from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Service, GalleryImage

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