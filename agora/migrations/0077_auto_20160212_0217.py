# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-12 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0076_auto_20160211_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='question_answers',
        ),
        migrations.AddField(
            model_name='user',
            name='question_answer',
            field=models.ManyToManyField(related_name='question_answer', through='agora.Answer', to='agora.Question'),
        ),
    ]
