# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=200, null=True)),
                ('answer_date', models.DateTimeField(editable=False)),
            ],
            options={
                'verbose_name': 'resposta',
                'verbose_name_plural': 'respostas',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'escolha',
                'verbose_name_plural': 'escolhas',
            },
        ),
        migrations.CreateModel(
            name='InitialListQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name=b'Nome da lista')),
                ('select', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Lista de Quest\xf5es para o Home',
                'verbose_name_plural': 'Lista de Quest\xf5es para o Home',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.CharField(default=b'N\xc3\xa3o', max_length=3, verbose_name=b'Publicado?')),
                ('kind', models.CharField(choices=[(b'1', b'Conhe\xc3\xa7a'), (b'2', b'Resultados'), (b'3', b'Comunidade'), (b'4', b'Participe')], max_length=1, verbose_name=b'Tipo')),
                ('publ_date', models.DateTimeField(verbose_name=b'Data de publica\xc3\xa7\xc3\xa3o')),
                ('message', models.CharField(max_length=500, verbose_name=b'Recado')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name=b'Endere\xc3\xa7o')),
            ],
        ),
        migrations.CreateModel(
            name='MeuEspacoArtigo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=200, verbose_name=b'Usuario')),
                ('categoria', models.CharField(blank=True, max_length=20, verbose_name=b'Categoria')),
                ('publ_date', models.DateTimeField(verbose_name=b'Data de publica\xc3\xa7\xc3\xa3o')),
                ('link', models.URLField(blank=True, max_length=1000)),
                ('comentario', models.CharField(blank=True, max_length=200, verbose_name=b'Coment\xc3\xa1rio')),
                ('secao', models.CharField(blank=True, max_length=30, verbose_name=b'Se\xc3\xa7\xc3\xa3o')),
                ('arquivo', models.FileField(blank=True, max_length=2000000, upload_to=b'C:\\virtual-agora\\media')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[(b'1', b'One choice'), (b'2', b'Multipla Escolha'), (b'3', b'Texto')], max_length=1, verbose_name=b'Tipo')),
                ('question_text', models.CharField(max_length=200, verbose_name=b'T\xc3\xadtulo da Quest\xc3\xa3o')),
                ('publ_date', models.DateTimeField(verbose_name=b'Data de publica\xc3\xa7\xc3\xa3o')),
                ('exp_date', models.DateTimeField(verbose_name=b'Data de expira\xc3\xa7\xc3\xa3o')),
                ('days', models.IntegerField(choices=[(1, b'1 dia'), (7, b'1 semana'), (30, b'1 m\xc3\xaas'), (365, b'1 ano'), (3650, b'Indeterminado')], default=3650, verbose_name=b'Tempo para expirar')),
                ('question_status', models.CharField(choices=[(b'n', b'N\xc3\xa3o publicado'), (b'p', b'Publicado')], default=b'p', max_length=1, verbose_name=b'Estado da quest\xc3\xa3o')),
                ('answer_status', models.CharField(choices=[(b'n', b'N\xc3\xa3o publicado'), (b'p', b'Publicado')], default=b'n', max_length=1, verbose_name=b'Estado da resposta')),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'question_images', verbose_name=b'Imagem')),
                ('address', models.CharField(max_length=200, verbose_name=b'Endere\xc3\xa7o')),
                ('permissao', models.IntegerField(default=0)),
                ('resultado', models.CharField(choices=[(b'n', b'N\xc3\xa3o publicado'), (b'p', b'Publicado')], default=b'n', max_length=1)),
            ],
            options={
                'verbose_name': 'quest\xe3o',
                'verbose_name_plural': 'quest\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Termo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(default=b'N\xc3\xa3o', max_length=3, verbose_name=b'Condi\xc3\xa7\xc3\xa3o')),
            ],
        ),
    ]
