# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-02 02:00
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conheca', '0003_auto_20160201_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article',
            field=ckeditor.fields.RichTextField(verbose_name='Descrição'),
        ),
    ]
