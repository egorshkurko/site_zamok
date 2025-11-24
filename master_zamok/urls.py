from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
]

# Раздача статических файлов в development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
else:
    # В production статические файлы должны раздаваться через веб-сервер (nginx/apache)
    # Но для работы админки можно временно включить раздачу через Django
    from django.contrib.staticfiles.views import serve
    from django.views.static import serve as static_serve
    from django.urls import re_path
    
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'insecure': True}),
        re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]