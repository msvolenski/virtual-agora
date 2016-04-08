# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import User, Answer, Termo, MeuEspaco, Message
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
# Register your models here.

class AnswerAdmin(admin.ModelAdmin):
  actions = ['show_results']
  list_display = ['userd', 'question', '__str__']
  list_filter = ['question', 'choice']

  def show_results(self, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return render(request, 'admin/resultados_admin.html', {'objects': queryset} )
  show_results.short_description = "Mostrar resultados"


class TermoAdmin(admin.ModelAdmin):
  list_display = ['userd', 'condition']

class MeuEspacoAdmin(admin.ModelAdmin):
  list_display = ['user', 'secao', 'categoria', 'publ_date','comentario','link','arquivo']

class MessageAdmin(admin.ModelAdmin):
    actions=['publicar_no_mural','desfazer_publicacao_no_mural']
    fields = ['kind','message','publ_date']
    list_display = ['kind','message','published','publ_date','address']

    def publicar_no_mural(modeladmin, request, queryset):
            queryset.update(published = 'Sim')
            queryset.update(publ_date = timezone.now())
            return

    def desfazer_publicacao_no_mural(modeladmin, request, queryset):
            queryset.update(published = 'Não')
            return


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Termo, TermoAdmin)
admin.site.register(MeuEspaco, MeuEspacoAdmin)
admin.site.register(Message, MessageAdmin)
