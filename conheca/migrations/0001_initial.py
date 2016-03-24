# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-24 00:32
from __future__ import unicode_literals

import ckeditor_uploader.fields
import conheca.models
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título do artigo')),
                ('article', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Descrição')),
                ('publ_date', models.DateTimeField(verbose_name='Data de publicação')),
                ('destaque', models.CharField(default='Não', max_length=3, verbose_name='Destacado?')),
                ('questao_associada', models.CommaSeparatedIntegerField(blank=True, max_length=100)),
                ('address', models.CharField(max_length=200, verbose_name='Endereço')),
                ('published', models.CharField(default='Não', max_length=3, verbose_name='Publicado?')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Artigos',
                'verbose_name': 'Artigo',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=1000)),
                ('url_title', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='SubTopico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtopico_nome', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Sub-tópicos',
                'verbose_name': 'Sub-topico',
            },
        ),
        migrations.CreateModel(
            name='Topico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField(max_length=200)),
                ('address_topico', models.CharField(max_length=200)),
                ('position', models.IntegerField(default=conheca.models.Topico.position_det)),
            ],
            options={
                'verbose_name_plural': 'Tópicos',
                'verbose_name': 'Tópico',
            },
        ),
        migrations.AddField(
            model_name='subtopico',
            name='subtopico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conheca.Topico'),
        ),
        migrations.AddField(
            model_name='link',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conheca.SubTopico'),
        ),
    ]
