# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-12 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0022_choice_usuario_que_votou'),
    ]

    operations = [
        migrations.AddField(
            model_name='questoesrespondidas',
            name='voto',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
