# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-16 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0034_auto_20160116_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='ano_de_ingresso',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='curso',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='faculdade',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nome',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
