# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20160212_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='text',
            field=models.TextField(max_length=1000, verbose_name='Texto'),
        ),
    ]