# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-01 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0067_remove_choice_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='ano_de_ingresso',
            field=models.CharField(default='ano', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='curso',
            field=models.CharField(default='curso', max_length=20),
        ),
    ]
