# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-23 20:28
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20160215_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='topicanswer',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Resposta'),
        ),
    ]