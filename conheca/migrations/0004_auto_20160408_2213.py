# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conheca', '0003_auto_20160408_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topico',
            name='projeto',
            field=models.CharField(choices=[('pdp-u', 'pdp-u'), ('RCB', 'RCB')], max_length=50, verbose_name=b'Projeto'),
        ),
    ]
