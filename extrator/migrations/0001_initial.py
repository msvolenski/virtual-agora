# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-10 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DadosPreproc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palavras_texto_original', models.CharField(max_length=10, verbose_name='PalavrasTO')),
                ('palavras_texto_lematizado', models.CharField(max_length=10, verbose_name='PalavrasTL')),
                ('palavras_texto_lematizado_ssw', models.CharField(max_length=10, verbose_name='PalavrasTLSSW')),
            ],
        ),
        migrations.CreateModel(
            name='ListaVertices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node', models.CharField(max_length=50, verbose_name='Node')),
                ('index', models.IntegerField(default=-1, verbose_name='index')),
            ],
        ),
        migrations.CreateModel(
            name='TabelaRanking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vertice_nome', models.CharField(max_length=60, verbose_name='V_nome')),
                ('vertice_numero', models.IntegerField(verbose_name='V_numero')),
                ('grau', models.IntegerField(verbose_name='Grau')),
                ('betweenness', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Betweenness')),
                ('closeness', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Closeness')),
            ],
        ),
        migrations.CreateModel(
            name='TextoPreproc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vertice', models.CharField(max_length=50, verbose_name='Vertice')),
                ('vertice_num', models.IntegerField()),
            ],
        ),
    ]