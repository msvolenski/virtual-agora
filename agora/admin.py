# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as AuthUser
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Choice, Question, Answer, User, InitialListQuestion, Message, Termo, MeuEspacoArtigo
from forum.models import User as ForumUser


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

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

class QuestionAdmin(admin.ModelAdmin):
  fields = ['question_text', 'image', ('question_type', 'days'), ('tags', 'question_status', 'answer_status')]
  inlines = [ChoiceInline]
  list_filter = ['publ_date', 'exp_date', 'question_type']
  search_fields = ['question_text']
  list_display = ['question_text', 'id', 'publ_date', 'exp_date', 'question_type', 'is_question_published', 'is_answer_published','address']
  actions = ['publish_question', 'unpublish_question']

  def publish_question(self, request, queryset):
    rows_updated = queryset.update(question_status='p')
    if rows_updated == 1:
      message_bit = "1 questão foi publicada"
    else:
      message_bit = "%s questões foram publicadas" % rows_updated
    self.message_user(request, "%s com sucesso." % message_bit)
  publish_question.short_description = "Publicar questões"

  def unpublish_question(self, request, queryset):
    rows_updated = queryset.update(question_status='n')
    if rows_updated == 1:
      message_bit = "1 questão foi despublicada"
    else:
      message_bit = "%s questões foram despublicadas" % rows_updated
    self.message_user(request, "%s com sucesso." % message_bit)
  unpublish_question.short_description = "Despublicar questões"


class UserProfileInline(admin.StackedInline):
  model = User
  can_delete = False
  verbose_name_plural = 'perfil pessoal'


class UserProfileInline2(admin.StackedInline):
  model = ForumUser
  can_delete = False
  verbose_name_plural = 'perfil do fórum'


class UserAdmin(UserAdmin):
    """Define a new UserAdmin"""
    inlines = [UserProfileInline, UserProfileInline2]

class AnswerAdmin(admin.ModelAdmin):
  actions = ['show_results']
  list_display = ['userd', 'question', '__str__']
  list_filter = ['question', 'choice']

  def show_results(self, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return render(request, 'admin/resultados_admin.html', {'objects': queryset} )
  show_results.short_description = "Mostrar resultados"

class InitialListQuestionAdmin(admin.ModelAdmin):
    actions = ['ativar_lista','desativar_lista']
    list_display = ['name','questoes','is_list_active']
    fields = ['name','questions',]


    def questoes(self, post):
        tags = []
        for tag in InitialListQuestion.questions.all():
            tags.append(str(tag))
        return ', '.join(tags)


    def ativar_lista(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Selecione apenas uma lista")
            return
        else:
            InitialListQuestion.objects.all().update(select=0)
            queryset.update(select = 1)
            return

    def desativar_lista(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Selecione apenas uma lista")
            return
        else:
            queryset.update(select = 0)
            return

class TermoAdmin(admin.ModelAdmin):
  list_display = ['userd', 'condition']

class MeuEspacoArtigoAdmin(admin.ModelAdmin):
  list_display = ['user', 'secao', 'categoria', 'publ_date','comentario','link','arquivo']


# Remove default User page and activate the new version
admin.site.unregister(AuthUser)
admin.site.register(AuthUser, UserAdmin)
admin.site.register(MeuEspacoArtigo, MeuEspacoArtigoAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Termo, TermoAdmin)
admin.site.register(InitialListQuestion, InitialListQuestionAdmin)
