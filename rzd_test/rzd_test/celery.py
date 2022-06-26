import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rzd_test.settings")
app = Celery("rzd_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
