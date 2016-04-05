# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import timezone
from agora.models import Message

from .models import Category, Topic, TopicAnswer, Like


class TopicAdmin(admin.ModelAdmin):
  actions = ['publicar_topico']
  fields = ['category', 'title', 'text', 'tags']
  list_filter = ['pub_date']
  list_display = ['category', 'title','published','text', 'pub_date']

  def publicar_topico(modeladmin, request, queryset):
          queryset.update(published = 'Sim')
          queryset.update(pub_date = timezone.now())
          x = Message(kind='3', published='Sim', publ_date=timezone.now())
          for title in queryset:
              t = title.title
              a = title.id
          x.message="Novo tópico inserido: {id}".format(id=t)
          x.address = a
          x.save()
          return


class TopicAnswerAdmin(admin.ModelAdmin):
  # fields = ['topic', 'text']
  list_filter = ['answer_date']
  list_display = ['user', 'topic', 'text', 'answer_date']


class LikeAdmin(admin.ModelAdmin):
  list_display = ['user', 'answer']


admin.site.register(Category)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicAnswer, TopicAnswerAdmin)
admin.site.register(Like, LikeAdmin)
