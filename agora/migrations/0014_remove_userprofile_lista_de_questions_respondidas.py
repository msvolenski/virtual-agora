# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 18:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0013_auto_20160105_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='lista_de_questions_respondidas',
        ),
    ]
