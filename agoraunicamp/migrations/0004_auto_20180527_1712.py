# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-27 20:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0003_auto_20180527_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='address',
        ),
        migrations.RemoveField(
            model_name='question',
            name='id',
        ),
        migrations.RemoveField(
            model_name='question',
            name='projeto',
        ),
        migrations.RemoveField(
            model_name='question',
            name='publ_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='published',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tags',
        ),
        migrations.AddField(
            model_name='question',
            name='publicacao_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='agoraunicamp.Publicacao'),
            preserve_default=False,
        ),
    ]
