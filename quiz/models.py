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
    right_answer = models.ForeignKey('quiz.Answer', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('quiz.Category', on_delete=models.SET_NULL, blank=True, null=True)


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


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
