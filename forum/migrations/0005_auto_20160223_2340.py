# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-23 23:40
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20160223_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Usuário ativo'),
        ),
        migrations.AlterField(
            model_name='topicanswer',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name=''),
        ),
    ]
