# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Relatorio
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from agora.models import Question

class Relatorio_geralAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Conteúdo', {'fields': ['conteudo']}),
        ('Tags', {'fields': ['tags']}),
        ('Data de Pubicação:', {'fields': ['publ_date']}),
        ('URL da página do Relatório:', {'fields': ['address']}),
    ]

    list_display = ['title', 'id', 'publ_date', 'published']

class RelatorioAdmin(admin.ModelAdmin):
    actions = ['publicar','desfazer_publicacao']
    fieldsets = [
        ('Tipo',               {'fields': ['tipo']}),
        (None,               {'fields': ['questao']}),
        ('Tags', {'fields': ['tags']}),
        ('Título', {'fields': ['titulo']}),
        ('Conteúdo', {'fields': ['conteudo']}),
    ]

    list_display = ['titulo','questao','id','publ_date', 'published','address']

    def publicar(modeladmin, request, queryset):
            if queryset.count() != 1:
                modeladmin.message_user(request, "Não é possível publicar mais de um relatório por vez.")
                return
            else:
                queryset.update(published = 'Sim')
                queryset.update(publ_date = timezone.now())
                queryset.update(publhistorico = 'Sim')

                for object in queryset:
                    if object.tipo == '2':
                        ids=object.questao.id
                        a = Question.objects.get(id=ids)
                        a.answer_status = 'p' #atualiza variaivel de question que indica se foi publicado
                        a.save()
                        return

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
