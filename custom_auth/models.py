from django.db import models

from base.models import TimeStampedModel


class VerificationCode(TimeStampedModel):

    email = models.EmailField(verbose_name='Электронная почта')
    code = models.CharField(verbose_name='Код подтверждения', max_length=30)
    is_active = models.BooleanField(verbose_name='Является ли действительным', default=True)
    expire_at = models.DateTimeField(verbose_name='Действует до')

    created = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='Время изменения', auto_now=True)

    class Meta:
        verbose_name = 'Код подтверждение email'
        verbose_name_plural = 'Коды подтверждение email'
        db_table = 'verification_code'
