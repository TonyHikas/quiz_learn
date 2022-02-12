from django.contrib.postgres.fields import ArrayField
from django.db import models


class Question(models.Model):
    text = models.TextField(
        null=True,
        blank=True
    )
    images = ArrayField(
        models.URLField(),
        verbose_name='Изображения'
    )
    category = models.ForeignKey(
        'quiz.Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


class Answer(models.Model):
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


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
