# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import User, Answer, Termo
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

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Termo, TermoAdmin)
