# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-19 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0051_auto_20170616_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrosdeajuste',
            name='num_tweets',
            field=models.IntegerField(default=100, verbose_name='N\xfamero de Tweets'),
        ),
    ]