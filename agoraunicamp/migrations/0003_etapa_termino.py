# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-05 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0002_auto_20180605_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='termino',
            field=models.TextField(default='null', verbose_name='Termino'),
        ),
    ]
