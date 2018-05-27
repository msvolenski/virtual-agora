# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class TopicAdmin(admin.ModelAdmin):
  actions = ['publicar_topico','remover_topico']
  fields = ['projeto', 'title', 'text', 'tags']
  list_filter = ['projeto','publ_date']
  list_display = ['projeto', 'title','text', 'published','publ_date']

  def remover_topico(modeladmin, request, queryset):
      if queryset.count() != 1:
        modeladmin.message_user(request, "Não é possível remover mais de um tópico por vez.")
        return
      else:         
        queryset.delete()                  
        return
      return

  def publicar_topico(modeladmin, request, queryset):
          queryset.update(published = 'Sim')
          queryset.update(publ_date = timezone.now())         
          return

  def get_project(self, obj):
      return obj.category.projeto.sigla
  
  get_project.short_description = 'Projeto'


class TopicAnswerAdmin(admin.ModelAdmin):
  list_filter = ['answer_date']
  list_display = ['user', 'topic', 'text', 'answer_date']


class EtapaAdmin(admin.ModelAdmin):
  list_display = ['project', 'etapa','name', 'header_txt', 'objetivo_txt','participar_txt','resultado_txt']


class AnswerAdmin(admin.ModelAdmin):
  actions = ['show_results']
  list_display = ['userd','user_stf','user_inst','question', '__str__']
  list_filter = ['question','user__institute','user__staff' ]

  def show_results(self, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return render(request, 'admin/resultados_admin.html', {'objects': queryset} )
  show_results.short_description = "Mostrar resultados"


class TermoAdmin(admin.ModelAdmin):
  list_display = ['userd', 'condition']


class MeuEspacoAdmin(admin.ModelAdmin):
  list_filter = ['projeto']
  list_display = ['projeto','user', 'secao', 'categoria', 'publ_date','comentario','link','arquivo']


class ProjetoAdmin(admin.ModelAdmin):        
  list_display = ['projeto','etapa_prj', 'sigla']


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
        ('Data de Pubicação:', {'fields': ['publ_date']}),
    ]
    list_display = ('projeto', 'title', 'id', 'publ_date', 'published','destaque', 'address')

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

#admin.site.disable_action('delete_selected')
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
  fields = ['projeto','question_text', 'question_type', 'tags', 'days']
  inlines = [ChoiceInline]
  list_filter = ['publ_date', 'exp_date', 'question_type']
  search_fields = ['question_text']
  list_display = ['projeto', 'question_text', 'id', 'publ_date', 'exp_date', 'question_type', 'is_question_published', 'is_answer_published','address']
  actions = ['publish_question', 'unpublish_question','remover_questao']

  def publish_question(self, request, queryset):
    if queryset.count() != 1:
        message_bit = "Não é possível publicar mais de uma questão por vez."
        self.message_user(request, message_bit)
        return
    else:
        queryset.update(question_status='p')
        message_bit = "Questão publicada"
        queryset.update(publ_date = timezone.now())
       
        self.message_user(request, message_bit)
        return
  publish_question.short_description = "Publicar questão"

  def remover_questao(modeladmin, request, queryset):
      if queryset.count() != 1:
          modeladmin.message_user(request, "Não é possível remover mais de uma questão por vez.")
          return
      else:
          for title in queryset:
              e = title.address
          objs = Message.objects.filter(kind = '4')
          for obj in objs:
              if obj.address == e:
                  queryset.delete()
                  obj.delete()
                  modeladmin.message_user(request, "Questão removida com sucesso.")
                  return
      return

  def unpublish_question(modeladmin, request, queryset):
    rows_updated = queryset.update(question_status='n')
    if queryset.count() != 1:
        modeladmin.message_user(request, "Não é possível remover mais de uma questão por vez.")
        return
    else:
        for title in queryset:
            e = title.address
        objs = Message.objects.filter(kind = '4')
        for obj in objs:
            if obj.address == e:
                obj.delete()
                modeladmin.message_user(request, "Questão despublicada com sucesso.")
                return
    return

  unpublish_question.short_description = "Despublicar questão"


class UserProfileInline(admin.StackedInline):
  model = User
  can_delete = False
  verbose_name_plural = 'perfil pessoal'


class UserProfileInline2(admin.StackedInline):
  model = User
  can_delete = False
  verbose_name_plural = 'perfil do fórum'


class UserAdmin(UserAdmin):  
    inlines = [UserProfileInline, UserProfileInline2]


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
    actions = ['publicar','desfazer_publicacao','remover_relatorio']
    fieldsets = [
        ('Selecione o projeto',               {'fields': ['projeto']}),
        ('Tipo',               {'fields': ['tipo']}),
        (None,               {'fields': ['questao']}),
        ('Tags', {'fields': ['tags']}),
        ('Título', {'fields': ['titulo']}),
        ('Conteúdo', {'fields': ['conteudo']}),
    ]

    list_display = ['projeto', 'titulo','questao','id','publ_date', 'published','address']

    def remover_relatorio(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível remover mais de um relatório por vez.")
            return
        else:
            for title in queryset:
                e = title.address
            objs = Message.objects.filter(kind = '2')
            for obj in objs:
                if obj.address == e:
                    queryset.delete()
                    obj.delete()
                    modeladmin.message_user(request, "Relatório removido com sucesso.")
                    return
        return

    def publicar(modeladmin, request, queryset):
            if queryset.count() != 1:
                modeladmin.message_user(request, "Não é possível publicar mais de um relatório por vez.")
                return
            else:
                queryset.update(published = 'Sim')
                queryset.update(publ_date = timezone.now())
                queryset.update(publhistorico = 'Sim')                
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
            for title in queryset:
                e = title.address
            objs = Message.objects.filter(kind = '2')
            for obj in objs:
                if obj.address == e:
                    obj.delete()
                    modeladmin.message_user(request, "Relatório despublicado com sucesso.")
                    return
            return



admin.site.register(Etapa, EtapaAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Termo, TermoAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(MeuEspaco, MeuEspacoAdmin)
admin.site.unregister(AuthUser)
admin.site.register(AuthUser, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Relatorio, RelatorioAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicAnswer, TopicAnswerAdmin)

