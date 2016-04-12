# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 00:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='projeto',
            field=models.CharField(choices=[('PDP-U', 'PDP-U')], max_length=50, verbose_name='Projeto'),
        ),
        migrations.AlterField(
            model_name='meuespaco',
            name='projeto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projeto_meu_espaco', to='agoraunicamp.Projeto'),
        ),
    ]
