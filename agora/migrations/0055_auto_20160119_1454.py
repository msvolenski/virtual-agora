# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-19 16:54
from __future__ import unicode_literals

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0054_auto_20160119_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(default=builtins.id, max_length=200),
        ),
    ]
