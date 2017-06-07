# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0029_protofrasesnew_temasnew'),
    ]

    operations = [
        migrations.AddField(
            model_name='protofrasesnew',
            name='extracao',
            field=models.TextField(default='nao', verbose_name='Extraiu?'),
        ),
        migrations.AddField(
            model_name='protofrasesnew',
            name='frase',
            field=models.TextField(default=1, verbose_name='Frase extraida'),
            preserve_default=False,
        ),
    ]