# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 19:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0028_counter'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Counter',
        ),
    ]
