"""Конфигурация приложение content."""
from django.apps import AppConfig


class ContentConfig(AppConfig):
    """Класс конфигурации приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'
