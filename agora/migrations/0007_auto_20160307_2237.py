# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0006_auto_20160229_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='institute',
            field=models.CharField(blank=True, max_length=40, verbose_name='Instituto'),
        ),
        migrations.AlterField(
            model_name='user',
            name='academic_registry',
            field=models.IntegerField(default=0, verbose_name='Registro acadêmico'),
        ),
        migrations.AlterField(
            model_name='user',
            name='course',
            field=models.CharField(blank=True, max_length=40, verbose_name='Curso'),
        ),
        migrations.AlterField(
            model_name='user',
            name='year_of_start',
            field=models.IntegerField(blank=True, verbose_name='Ano de ingresso'),
        ),
    ]
