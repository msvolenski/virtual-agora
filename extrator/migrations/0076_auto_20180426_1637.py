# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0075_auto_20180426_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temasnew',
            name='irt_l',
            field=models.FloatField(verbose_name='IRT Local (%)'),
        ),
    ]
