# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-30 00:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0011_auto_20180529_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nome_completo',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nome Completo'),
        ),
    ]
