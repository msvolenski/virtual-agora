# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-18 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0044_auto_20160116_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votodousuario',
            name='faculdade',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
