# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-23 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0061_auto_20180322_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extracaonew',
            name='irgs_p',
            field=models.TextField(verbose_name='IRGS%'),
        ),
        migrations.AlterField(
            model_name='extracaonew',
            name='irse_p',
            field=models.TextField(verbose_name='IRSE%'),
        ),
    ]