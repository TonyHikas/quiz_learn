# Generated by Django 4.0.1 on 2022-03-26 15:02

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('text', models.TextField(blank=True, null=True)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), default=[], size=None, verbose_name='Изображения')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.category')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('text', models.CharField(max_length=255, verbose_name='Тест ответа')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Пояснение ответа')),
                ('right', models.BooleanField(default=False, verbose_name='Является ли ответ правильным')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
                'db_table': 'answer',
            },
        ),
    ]
