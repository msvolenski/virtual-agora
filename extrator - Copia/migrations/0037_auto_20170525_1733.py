# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-25 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0036_auto_20170525_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosextracaonew',
            name='irgs',
            field=models.FloatField(default=1, verbose_name='IRGS'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dadosextracaonew',
            name='irgs_p',
            field=models.FloatField(default=1, verbose_name='IRGS%'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dadosextracaonew',
            name='irse',
            field=models.FloatField(default=1, verbose_name='IRSE'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dadosextracaonew',
            name='irse_p',
            field=models.FloatField(default=1, verbose_name='IRSE%'),
            preserve_default=False,
        ),
    ]