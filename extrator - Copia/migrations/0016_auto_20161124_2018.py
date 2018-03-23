# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-24 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0015_paragrafosextraidos'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragrafosextraidos',
            name='etapa',
            field=models.IntegerField(default=1, verbose_name='etapa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paragrafosextraidos',
            name='protofrase_original',
            field=models.TextField(default=1, verbose_name='proto-frase_original'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paragrafosextraidos',
            name='protofrase',
            field=models.TextField(verbose_name='Proto-Frase_atual'),
        ),
    ]