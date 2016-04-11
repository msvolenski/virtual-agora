# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as AuthUser
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Choice, Question, InitialListQuestion
from agoraunicamp.models import User, Message
from forum.models import User as ForumUser


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
  fields = ['projeto','question_text', 'question_type', 'tags', 'days']
  inlines = [ChoiceInline]
  list_filter = ['publ_date', 'exp_date', 'question_type']
  search_fields = ['question_text']
  list_display = ['projeto', 'question_text', 'id', 'publ_date', 'exp_date', 'question_type', 'is_question_published', 'is_answer_published','address']
  actions = ['publish_question', 'unpublish_question']

  def publish_question(self, request, queryset):
    if queryset.count() != 1:
        message_bit = "Não é possível publicar mais de uma questão por vez."
        self.message_user(request, message_bit)
        return
    else:
        queryset.update(question_status='p')
        message_bit = "Questão publicada"
        queryset.update(publ_date = timezone.now())
        x = Message(kind='4', published='Sim', publ_date=timezone.now())
        for title in queryset:
            t = title.question_text
            a = title.address
            p = title.projeto
        x.message="Nova questão inserida: {id}".format(id=t)
        x.address = a
        x.projeto = p
        x.save()
        self.message_user(request, message_bit)
        return
  publish_question.short_description = "Publicar questão"


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


class InitialListQuestionAdmin(admin.ModelAdmin):
    actions = ['ativar_lista','desativar_lista']
    list_display = ['projeto','name','questoes','is_list_active']
    fields = ['projeto','name','questions',]


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






# Remove default User page and activate the new version
admin.site.unregister(AuthUser)
admin.site.register(AuthUser, UserAdmin)

admin.site.register(Question, QuestionAdmin)
admin.site.register(InitialListQuestion, InitialListQuestionAdmin)
