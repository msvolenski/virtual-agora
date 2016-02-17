# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-12 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Theme',
            new_name='Category',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'categoria', 'verbose_name_plural': 'categorias'},
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='theme',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='user',
            name='topic_answers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='topic_answers_likes',
        ),
        migrations.AddField(
            model_name='user',
            name='topic_answer',
            field=models.ManyToManyField(related_name='topic_answer', through='forum.TopicAnswer', to='forum.Topic'),
        ),
        migrations.AddField(
            model_name='user',
            name='topic_answer_like',
            field=models.ManyToManyField(related_name='topic_answer_like', through='forum.Like', to='forum.TopicAnswer'),
        ),
    ]
