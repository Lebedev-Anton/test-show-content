"""Url для приложения content."""
from django.urls import path

from .views import index


urlpatterns = [
    path('', index),
]
