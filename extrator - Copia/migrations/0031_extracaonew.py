# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0030_auto_20170522_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtracaoNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protofrase', models.TextField(verbose_name='Proto Frase')),
                ('frase', models.TextField(verbose_name='Frase')),
            ],
        ),
    ]