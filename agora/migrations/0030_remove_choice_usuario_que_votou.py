# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-16 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0029_delete_counter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='usuario_que_votou',
        ),
    ]
