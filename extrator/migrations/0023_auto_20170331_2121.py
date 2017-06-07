# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 00:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0022_pesosealpha'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesosealpha',
            name='alphaesp',
            field=models.FloatField(default=1, verbose_name='Alphaesp'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pesosealpha',
            name='erro',
            field=models.FloatField(default=1, verbose_name='erro'),
            preserve_default=False,
        ),
    ]