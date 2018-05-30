# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-28 23:41
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0005_auto_20180528_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicAnswerReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='')),
                ('answer_date', models.DateTimeField(editable=False)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agoraunicamp.TopicAnswer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agoraunicamp.User')),
            ],
            options={
                'verbose_name': 'R\xe9plica',
                'verbose_name_plural': 'R\xe9plicas',
            },
        ),
    ]
