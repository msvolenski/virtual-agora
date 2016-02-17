from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Link, Article, Topico, SubTopico


class LinkInline(admin.TabularInline):
  model = Link
  extra = 1


class SubTopicoInline(admin.TabularInline):
  model = SubTopico
  extra = 1


class SubTopicoAdmin(admin.ModelAdmin):

  fieldsets = [
    (None, {'fields': ['subtopico']}),
  ]
  inlines = [LinkInline]


class TopicoAdmin(admin.ModelAdmin):
  actions = ['posicionar_topico']
  #actions = ['inverter_ordem_de_apresentacao']
  #setam os campos que irão aparecer no "Add adiciona Link"
  fieldsets = [
    (None,               {'fields': ['topico']}),
    ('URL da página do Tópico:', {'fields': ['address_topico']}),
    #('Data de publicação', {'fields': ['pub_date']}),
  ]

  inlines = [SubTopicoInline]
  list_display = ['topico','position','id']
  search_fields = ['topico']

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
  list_filter = ['tags']
  actions = ['destacar_artigo','publicar_na_pagina_principal','desfazer_publicacao_na_pagina_principal','mostrar_o_artigo']
  fieldsets = [
    (None, {'fields': ['title']}),
    ('Conteúdo', {'fields': ['article']}),
    ('Tags', {'fields': ['tags']}),
    ('Questões associada a este Artigo', {'fields': ['questao_associada']}),
    ('Data de Pubicação:', {'fields': ['publ_date']}),
    ('URL da página do Artigo:', {'fields': ['address']}),
  ]
  list_display = ('title', 'id', 'publ_date', 'questao_associada', 'published','destaque')

  def destacar_artigo(modeladmin, request, queryset):
    if queryset.count() != 1:
      modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
    else:
      Article.objects.all().update(destaque = 'Não')
      queryset.update(destaque = 'Sim')

  def publicar_na_pagina_principal(modeladmin, request, queryset):
    queryset.update(published = 'Sim')
    queryset.update(publ_date = timezone.now())

  def desfazer_publicacao_na_pagina_principal(modeladmin, request, queryset):
    queryset.update(published = 'Não')

  def mostrar_o_artigo(modeladmin, request, queryset):
   if queryset.count() != 1:
    modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
    return
   else:
     selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
     ct = ContentType.objects.get_for_model(queryset.model)
     return HttpResponseRedirect("http://127.0.0.1:8000/agora/pdpu/conheca/artigos/%s%s" % ( "", ",".join(selected)) )
    #return HttpResponseRedirect("http://127.0.0.1:8000/agora/pdpu/conheca/artigos/%s&ids=%s")


admin.site.register(Topico, TopicoAdmin )
admin.site.register(SubTopico, SubTopicoAdmin )
admin.site.register(Article, ArticleAdmin )
