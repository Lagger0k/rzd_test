from django.db import models


class JsonFileFromExcel(models.Model):
    """Модель для хранения информации об обработанных excel файлах."""
    file_name = models.CharField(verbose_name='file_name', max_length=255)
    file_body = models.JSONField(verbose_name='file_body')
