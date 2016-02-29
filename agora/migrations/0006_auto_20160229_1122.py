# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-29 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('agora', '0005_auto_20160223_1133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='initiallistquestion',
            options={'verbose_name': 'Lista de Questões para o Home', 'verbose_name_plural': 'Lista de Questões para o Home'},
        ),
        migrations.AlterField(
            model_name='initiallistquestion',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nome da lista'),
        ),
        migrations.AlterField(
            model_name='initiallistquestion',
            name='questions',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Questões'),
        ),
        migrations.AlterField(
            model_name='question',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200, verbose_name='Título da Questão'),
        ),
    ]
