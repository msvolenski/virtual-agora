# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-29 17:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conheca', '0007_auto_20160128_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='AdicionaLink',
        ),
        migrations.AddField(
            model_name='link',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conheca.Topic'),
        ),
    ]
