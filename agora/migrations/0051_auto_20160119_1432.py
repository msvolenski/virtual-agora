# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-19 16:32
from __future__ import unicode_literals

import agora.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0050_auto_20160119_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='id',
        ),
      
    ]