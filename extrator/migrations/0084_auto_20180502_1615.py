# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-02 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0083_auto_20180502_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusters',
            name='caminho',
            field=models.TextField(default=1, verbose_name='Nucleos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clusters',
            name='ident',
            field=models.TextField(default=1, verbose_name='Identificacao'),
            preserve_default=False,
        ),
    ]