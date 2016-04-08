# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0003_meuespaco'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.CharField(default='N\xe3o', max_length=3, verbose_name='Publicado?')),
                ('kind', models.CharField(choices=[('1', 'Conhe\xe7a'), ('2', 'Resultados'), ('3', 'Comunidade'), ('4', 'Participe')], max_length=1, verbose_name='Tipo')),
                ('publ_date', models.DateTimeField(verbose_name='Data de publica\xe7\xe3o')),
                ('message', models.CharField(max_length=500, verbose_name='Recado')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='Endere\xe7o')),
            ],
        ),
    ]
