# Generated by Django 4.0.1 on 2022-05-08 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Является ли действительным'),
        ),
    ]
