# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-30 00:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0013_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='media/img/falcaobrega.jpg', upload_to='media/img/'),
        ),
    ]
