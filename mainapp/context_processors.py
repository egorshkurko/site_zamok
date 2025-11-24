"""
Context processors для глобального доступа к переменным в шаблонах
"""
from django.conf import settings


def contact_info(request):
    """Добавляет контактную информацию во все шаблоны"""
    return {
        'CONTACT_PHONE': settings.CONTACT_PHONE,
        'CONTACT_PHONE_TEL': settings.CONTACT_PHONE_TEL,
    }

