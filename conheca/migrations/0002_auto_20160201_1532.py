# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-01 17:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conheca', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='pub_date',
            new_name='publ_date',
        ),
    ]
