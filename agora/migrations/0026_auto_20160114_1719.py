# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-14 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0025_auto_20160112_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotoDoUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voto', models.CharField(max_length=200)),
                ('usuario', models.ManyToManyField(to='agora.Usuario')),
            ],
        ),
        migrations.RemoveField(
            model_name='questoesrespondidas',
            name='voto',
        ),
    ]
