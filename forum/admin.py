# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import timezone
from agoraunicamp.models import Message

from .models import Category, Topic, TopicAnswer, Like


class TopicAdmin(admin.ModelAdmin):
  actions = ['publicar_topico']
  fields = ['category', 'title', 'text', 'tags']
  list_filter = ['pub_date']
  list_display = ['get_project', 'title','text', 'published','pub_date']

  def publicar_topico(modeladmin, request, queryset):
          queryset.update(published = 'Sim')
          queryset.update(pub_date = timezone.now())
          x = Message(kind='3', published='Sim', publ_date=timezone.now())
          for title in queryset:
              t = title.title
              a = title.id
              p = title.projeto
          x.message="Novo tópico inserido: {id}".format(id=t)
          x.address = a
          x.projeto = p
          x.save()
          return

  def get_project(self, obj):
      return obj.category.projeto.sigla
  get_project.short_description = 'Projeto'



class TopicAnswerAdmin(admin.ModelAdmin):
  # fields = ['topic', 'text']
  list_filter = ['answer_date']
  list_display = ['user', 'topic', 'text', 'answer_date']


class LikeAdmin(admin.ModelAdmin):
  list_display = ['user', 'answer']

class CategoryAdmin(admin.ModelAdmin):
  list_display = ['projeto', 'title']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicAnswer, TopicAnswerAdmin)
admin.site.register(Like, LikeAdmin)
