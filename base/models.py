from django.db import models


class TimeStampedModel(models.Model):

    created = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='Время изменения', auto_now=True)

    class Meta:
        abstract = True
