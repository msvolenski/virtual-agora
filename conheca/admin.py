# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponseRedirect
from django.utils import timezone
from agoraunicamp.models import Message

from .models import Link, Article, Topico, SubTopico


class LinkInline(admin.TabularInline):
  model = Link
  extra = 1


class SubTopicoInline(admin.TabularInline):
  model = SubTopico
  extra = 1


class SubTopicoAdmin(admin.ModelAdmin):
  actions = ['remover_subtopico']
  fieldsets = [
    (None, {'fields': ['subtopico']}),
  ]
  inlines = [LinkInline]

  def remover_subtopico(modeladmin, request, queryset):
      if queryset.count() != 1:
          modeladmin.message_user(request, "Não é possível remover mais de um tópico por vez.")
          return
      else:
          queryset.delete()
      return


class TopicoAdmin(admin.ModelAdmin):
  actions = ['posicionar_topico', 'remover_topico']
  #actions = ['inverter_ordem_de_apresentacao']
  #setam os campos que irão aparecer no "Add adiciona Link"
  fieldsets = [
    ('Selecione o Projeto',               {'fields': ['projeto']}),
    (None,               {'fields': ['topico']}),

    #('Data de publicação', {'fields': ['pub_date']}),
  ]

  inlines = [SubTopicoInline]
  list_display = ['topico','position','id','address_topico',]
  search_fields = ['topico']

  def remover_topico(modeladmin, request, queryset):
      if queryset.count() != 1:
          modeladmin.message_user(request, "Não é possível remover mais de um tópico por vez.")
          return
      else:
          queryset.delete()
      return


  def posicionar_topico(modeladmin, request, queryset):
    if queryset.count() != 2:
      modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
    else:
      a = queryset.first()
      a1 = a.position
      b = queryset.last()
      b1 = b.position
      queryset.filter(id=a.pk).update(position = b1)
      queryset.filter(id=b.pk).update(position = a1)


class ArticleAdmin(admin.ModelAdmin):

    def delete_selected(self, request):
        return False

    list_filter = ['projeto','tags']
    actions = ['destacar_artigo','publicar_na_pagina_principal','desfazer_publicacao_na_pagina_principal','mostrar_o_artigo','remover_artigo']
    fieldsets = [

        ('Selecione o Projeto',               {'fields': ['projeto']}),
        (None,               {'fields': ['title']}),

        ('Conteúdo', {'fields': ['article']}),
        ('Tags', {'fields': ['tags']}),
        ('Questões associada a este Artigo', {'fields': ['questao_associada']}),
        ('Data de Pubicação:', {'fields': ['publ_date']}),

    ]


    list_display = ('projeto', 'title', 'id', 'publ_date', 'questao_associada', 'published','destaque', 'address')


    def remover_artigo(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível remover mais de um artigo por vez.")
            return
        else:
            for title in queryset:
                e = title.address
            objs = Message.objects.filter(kind = '1')
            for obj in objs:
                if obj.address == e:
                    queryset.delete()
                    obj.delete()
                    modeladmin.message_user(request, "Artigo removido com sucesso.")
                    return
        return





    def destacar_artigo(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
            return
        else:
            Article.objects.all().update(destaque = 'Não')
            queryset.update(destaque = 'Sim')

            return

    def publicar_na_pagina_principal(modeladmin, request, queryset):
            queryset.update(published = 'Sim')
            queryset.update(publ_date = timezone.now())
            x = Message(kind='1',message="Novo artigo inserido:{id}", published='Sim', publ_date=timezone.now())
            for title in queryset:
                t = title.title
                a = title.address
                p = title.projeto
            x.message="Novo artigo inserido: {id}".format(id=t)
            x.projeto = p
            x.address = a
            x.save()
            return

    def desfazer_publicacao_na_pagina_principal(modeladmin, request, queryset):
            queryset.update(published = 'Não')
            return

    def mostrar_o_artigo(modeladmin, request, queryset):
         if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
            return
         else:
             selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
             ct = ContentType.objects.get_for_model(queryset.model)
             for article in queryset:
                 t = article.address
             return HttpResponseRedirect(t)
            #return HttpResponseRedirect("http://127.0.0.1:8000/agora/pdpu/conheca/artigos/%s&ids=%s")









          # a = queryset.values('address')
            #response = HttpResponse(content_type="www.uol.com.br")

            #return response



    #search_fields = ['titulo']


admin.site.register(Topico, TopicoAdmin )
admin.site.register(SubTopico, SubTopicoAdmin )
admin.site.register(Article, ArticleAdmin )
