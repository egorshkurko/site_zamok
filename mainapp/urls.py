from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path('contacts/', views.contacts, name='contacts'),
    path('garant/', views.garant, name='garant'),
    path('otziv/', views.otziv, name='otziv'),
    path('webhook/github/', views.github_webhook, name='github_webhook'),
]