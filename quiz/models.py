from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models import TimeStampedModel


class Question(TimeStampedModel):
    text = models.TextField(
        null=True,
        blank=True
    )
    images = ArrayField(
        models.URLField(),
        verbose_name='Изображения',
        default=list,
        blank=True,
        null=False
    )
    category = models.ForeignKey(
        'quiz.Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'question'

    def __str__(self):
        return self.text


class Answer(TimeStampedModel):
    text = models.CharField(
        max_length=255,
        verbose_name='Тест ответа'
    )
    description = models.TextField(
        verbose_name='Пояснение ответа',
        null=True,
        blank=True
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        related_name='answers'
    )
    right = models.BooleanField(
        default=False,
        verbose_name='Является ли ответ правильным'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        db_table = 'answer'

    def __str__(self):
        return self.text


class Category(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category'

    def __str__(self):
        return self.name


