# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-19 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0015_auto_20160319_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='primeiro_nome',
            field=models.CharField(blank=True, max_length=40, verbose_name='Primeiro nome'),
        ),
        migrations.AddField(
            model_name='user',
            name='staff',
            field=models.CharField(blank=True, choices=[('1', 'Professor'), ('2', 'Funcionário'), ('3', 'Aluno'), ('4', 'Outro')], max_length=1, verbose_name='Staff'),
        ),
        migrations.AddField(
            model_name='user',
            name='ultimo_nome',
            field=models.CharField(blank=True, max_length=100, verbose_name='Sobrenome'),
        ),
    ]
