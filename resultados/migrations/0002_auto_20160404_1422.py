# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relatorio',
            name='destaque',
            field=models.CharField(default=b'N\xc3\xa3o', max_length=3),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='publhistorico',
            field=models.CharField(default=b'N\xc3\xa3o', max_length=3),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='published',
            field=models.CharField(default=b'N\xc3\xa3o', max_length=3),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='tipo',
            field=models.CharField(choices=[(b'1', b'Geral'), (b'2', b'Quest\xc3\xa3o')], default=b'1', max_length=10),
        ),
    ]