import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cgpu_connect.settings')

app = Celery('cgpu_connect')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
