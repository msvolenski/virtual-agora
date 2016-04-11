# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Relatorio
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from agora.models import Question
from agoraunicamp.models import Message


class Relatorio_geralAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Selecione o projeto',               {'fields': ['projeto']}),
        (None,               {'fields': ['title']}),
        ('Conteúdo', {'fields': ['conteudo']}),
        ('Tags', {'fields': ['tags']}),
        ('Data de Pubicação:', {'fields': ['publ_date']}),
        ('URL da página do Relatório:', {'fields': ['address']}),
    ]

    list_display = ['projeto','title', 'id', 'publ_date', 'published']

class RelatorioAdmin(admin.ModelAdmin):
    list_filter = ['projeto']
    actions = ['publicar','desfazer_publicacao']
    fieldsets = [
        ('Selecione o projeto',               {'fields': ['projeto']}),
        ('Tipo',               {'fields': ['tipo']}),
        (None,               {'fields': ['questao']}),
        ('Tags', {'fields': ['tags']}),
        ('Título', {'fields': ['titulo']}),
        ('Conteúdo', {'fields': ['conteudo']}),
    ]

    list_display = ['projeto', 'titulo','questao','id','publ_date', 'published','address']

    def publicar(modeladmin, request, queryset):
            if queryset.count() != 1:
                modeladmin.message_user(request, "Não é possível publicar mais de um relatório por vez.")
                return
            else:
                queryset.update(published = 'Sim')
                queryset.update(publ_date = timezone.now())
                queryset.update(publhistorico = 'Sim')
                x = Message(kind='2', published='Sim', publ_date=timezone.now())
                for title in queryset:
                    t = title.titulo
                    a = title.address
                    p = title.projeto
                x.message="Novo relatório inserido: {id}".format(id=t)
                x.address = a
                x.projeto = p
                x.save()
                message_bit = "Relatório publicado"
                modeladmin.message_user(request, message_bit)
                for object in queryset:
                    if object.tipo == '2':
                        ids=object.questao.id
                        a = Question.objects.get(id=ids)
                        a.answer_status = 'p' #atualiza variaivel de question que indica se foi publicado
                        a.save()
                        return
                return
    publicar.short_description = "Publicar relatório"



    def desfazer_publicacao(modeladmin, request, queryset):
        if queryset.count() != 1:
                modeladmin.message_user(request, "Não é possível desfazer a publicação de mais de um relatório por vez.")
                return
        else:
            queryset.update(published = 'Não')
            for object in queryset:
                if object.tipo == '2':
                    ids=object.questao.id
                    a = Question.objects.get(id=ids)
                    a.answer_status = 'n' #atualiza variaivel de question que indica se foi publicado
                    a.save()
                    return


admin.site.register(Relatorio, RelatorioAdmin )
