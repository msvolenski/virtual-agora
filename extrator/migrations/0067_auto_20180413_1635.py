# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-13 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0066_remove_dadosextracaonew_quantidade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dadosextracaonew',
            name='rep_geral',
        ),
        migrations.RemoveField(
            model_name='dadosextracaonew',
            name='rep_tema',
        ),
        migrations.AddField(
            model_name='dadosextracaonew',
            name='irgs_p',
            field=models.FloatField(default=1, verbose_name='IRGS%'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dadosextracaonew',
            name='irse_p',
            field=models.FloatField(default=1, verbose_name='IRSE%'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dadosextracaonew',
            name='quantidade',
            field=models.IntegerField(default=1, verbose_name='Quantidade'),
            preserve_default=False,
        ),
    ]