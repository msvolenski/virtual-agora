# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-13 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0062_auto_20180322_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrosdeajuste',
            name='radio_r',
            field=models.FloatField(default=0.0, verbose_name='Representatividade_minima'),
        ),
    ]
