# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-03 20:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agoraunicamp', '0017_auto_20180602_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposta_text', models.TextField(verbose_name='Proposta')),
            ],
            options={
                'verbose_name': 'prposta',
                'verbose_name_plural': 'propostas',
            },
        ),
        migrations.AddField(
            model_name='relatorio',
            name='propostas_org',
            field=models.CharField(choices=[('1', 'Da Quet\xe3o'), ('2', 'Dos campos abaixo')], default='1', max_length=3, verbose_name='Caso tenha selecionado PROPOSTAS, escolha a origem'),
        ),
        migrations.AddField(
            model_name='proposta',
            name='relatorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agoraunicamp.Relatorio'),
        ),
    ]
