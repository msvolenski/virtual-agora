# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class PropostaInline(admin.TabularInline):
    model = Proposta
    extra = 0

class TopicAdmin(admin.ModelAdmin):
  model = Topic
    
  def get_list_display(self, request):
    return ('projeto','etapa_publ', 'pk','title','text', 'published','publ_date')  
  
  actions = ['publicar_topico', 'despublicar_topico', 'remover_topico']
  list_filter = ['projeto','publ_date']

  def remover_topico(modeladmin, request, queryset):
      if queryset.count() != 1:
        modeladmin.message_user(request, "Não é possível remover mais de um tópico por vez.")
        return
      else:         
        queryset.delete()                  
        return

  def publicar_topico(modeladmin, request, queryset):
    queryset.update(published = 'sim')
    queryset.update(publ_date = timezone.now())         
    return

  def despublicar_topico(modeladmin, request, queryset):
    queryset.update(published = 'nao')                  
    return  
  
  def get_project(self, obj):
      return obj.category.projeto.sigla
  
  get_project.short_description = 'Projeto'


class TopicAnswerAdmin(admin.ModelAdmin):
  list_filter = ['answer_date']
  list_display = ['user', 'topic', 'text', 'answer_date']

class TopicAnswerReplyAdmin(admin.ModelAdmin):
  list_filter = ['answer_date']
  list_display = ['user', 'text', 'answer_date']

class CurtirAdmin(admin.ModelAdmin):
  list_filter = ['proposta']
  list_display = ['proposta', 'user']


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

class PropostaAdmin(admin.ModelAdmin):
    list_display = ['relatorio', 'proposta_text']


class MeuEspacoAdmin(admin.ModelAdmin):
  list_filter = ['projeto']
  list_display = ['projeto','user', 'secao', 'categoria', 'publ_date','comentario','link','arquivo']


class ProjetoAdmin(admin.ModelAdmin):        
  list_display = ['projeto','etapa_prj', 'sigla']


class ArticleAdmin(admin.ModelAdmin):    
    model = Article
    
    def get_list_display(self, request):
        return ('projeto', 'etapa_publ', 'pk', 'title', 'publ_date', 'published', 'address')    
   
    list_filter = ['projeto']
    actions = ['publicar_na_pagina_principal','desfazer_publicacao_na_pagina_principal','mostrar_o_artigo','remover_artigo']   

    def remover_artigo(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível remover mais de um artigo por vez.")
            return
        else:            
            queryset.delete()
            modeladmin.message_user(request, "Artigo removido com sucesso.")
            return

    def publicar_na_pagina_principal(modeladmin, request, queryset):
            queryset.update(published = 'sim')
            queryset.update(publ_date = timezone.now()) 
            return

    def desfazer_publicacao_na_pagina_principal(modeladmin, request, queryset):
            queryset.update(published = 'nao')
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

class QuestionAdmin(admin.ModelAdmin):
  model = Question
    
  def get_list_display(self, request):        
    return ('projeto', 'etapa_publ', 'pk', 'question_text', 'publ_date', 'exp_date','published','question_type','address')    
  
  #fields = ['projeto','question_text', 'question_type', 'tags','publ_date','exp_date']
  inlines = [ChoiceInline]
  list_filter = ['publ_date', 'exp_date', 'question_type']
  search_fields = ['question_text']
  #list_display = ['projeto', 'question_text', 'id', 'publ_date', 'exp_date','published','question_type','address']
  actions = ['publish_question', 'unpublish_question','remover_questao']

  def publish_question(self, request, queryset):
    if queryset.count() != 1:
        message_bit = "Não é possível publicar mais de uma questão por vez."
        self.message_user(request, message_bit)
        return
    else:
        queryset.update(published='sim')
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
          queryset.delete()
          modeladmin.message_user(request, "Questão removida com sucesso.")
          return    

  def unpublish_question(modeladmin, request, queryset):    
    if queryset.count() != 1:
        modeladmin.message_user(request, "Não é despublicar mais de uma questão por vez.")
        return
    else:
        queryset.update(published='nao')
        modeladmin.message_user(request, "Questão despublicada com sucesso.")
        return
  unpublish_question.short_description = "Despublicar questão"


class UserProfileInline(admin.StackedInline):
  model = User
  can_delete = False
  verbose_name_plural = 'perfil pessoal'
  

class UserAdmin(UserAdmin):  
    inlines = [UserProfileInline]


class RelatorioAdmin(admin.ModelAdmin):
    model = Relatorio
    
    def get_list_display(self, request):
        return ('projeto', 'etapa_publ', 'pk', 'titulo','questao', 'publ_date', 'published','grafico','arquivo') 
    
    inlines = [PropostaInline]
    list_filter = ['projeto']
    actions = ['publicar','desfazer_publicacao','remover_relatorio']
    
    def remover_relatorio(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível remover mais de um relatório por vez.")
            return
        else:            
            queryset.delete()                    
            modeladmin.message_user(request, "Relatório removido com sucesso.")
            return      

    def publicar(modeladmin, request, queryset):
            if queryset.count() != 1:
                modeladmin.message_user(request, "Não é possível publicar mais de um relatório por vez.")
                return
            else:
                queryset.update(published = 'sim')
                queryset.update(publ_date = timezone.now())                               
                message_bit = "Relatório publicado"
                modeladmin.message_user(request, message_bit)                
                return
    publicar.short_description = "Publicar relatório"

    def desfazer_publicacao(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível desfazer a publicação de mais de um relatório por vez.")
            return
        else:
            queryset.update(published = 'nao')
            modeladmin.message_user(request, "Relatório despublicado com sucesso.")
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
admin.site.register(TopicAnswerReply, TopicAnswerReplyAdmin)
admin.site.register(TopicAnswer, TopicAnswerAdmin)
admin.site.register(Proposta, PropostaAdmin)
admin.site.register(Curtir, CurtirAdmin)


