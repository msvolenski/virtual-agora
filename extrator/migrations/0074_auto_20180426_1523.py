# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0073_auto_20180426_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clusters',
            name='q_nucleos',
            field=models.IntegerField(null=True, verbose_name='Qtdd de N\xfacleos'),
        ),
        migrations.AlterField(
            model_name='clusters',
            name='q_subtemas',
            field=models.IntegerField(null=True, verbose_name='Qtdd de subtemas'),
        ),
    ]