# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 19:04
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('agora', '0014_remove_userprofile_lista_de_questions_respondidas'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
