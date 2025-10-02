import os

from celery import Celery

# Устанавливаем модуль настроек Django для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("src")

# Используем конфигурацию из настроек Django, с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживаем и регистрируем задачи из всех приложений Django
app.autodiscover_tasks()
