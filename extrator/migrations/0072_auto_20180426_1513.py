# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0071_clusters_situacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusters',
            name='etapa',
            field=models.IntegerField(default=1, verbose_name='Etapa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clusters',
            name='q_nucleos',
            field=models.IntegerField(default=1, verbose_name='Qtdd de N\xfacleos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clusters',
            name='q_subtemas',
            field=models.IntegerField(default=1, verbose_name='Qtdd de subtemas'),
            preserve_default=False,
        ),
    ]
