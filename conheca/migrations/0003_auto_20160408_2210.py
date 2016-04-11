# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 01:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conheca', '0002_article_projeto'),
    ]

    operations = [
        migrations.AddField(
            model_name='topico',
            name='projeto',
            field=models.CharField(choices=[(1, 'Plano Diretor Participativo'), (2, 'Reforma do Ciclo B\xe1sico')], default=b'none', max_length=50, verbose_name=b'Projeto'),
        ),
        migrations.AlterField(
            model_name='article',
            name='projeto',
            field=models.CharField(choices=[('pdp-u', 'pdp-u'), ('RCB', 'RCB')], max_length=50, verbose_name=b'Projeto'),
        ),
    ]
