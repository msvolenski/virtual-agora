# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 19:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0010_questoesrespondidas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questoesrespondidas',
            old_name='publications',
            new_name='usuario',
        ),
    ]
