from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as AuthUser
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .models import Choice, Question, Answer, User

class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 0


class QuestionAdmin(admin.ModelAdmin):
  fields = ['question_text', 'image', ('question_type', 'days'), ('tags', 'question_status', 'answer_status')]

  inlines = [ChoiceInline]

  list_filter = ['pub_date', 'exp_date', 'question_type']
  search_fields = ['question_text']
  list_display = ['question_text', 'id', 'pub_date', 'exp_date', 'question_type', 'is_question_published', 'is_answer_published']
  actions = ['publish_question', 'unpublish_question', 'publish_result', 'unpublish_result']

  def publish_question(self, request, queryset):
    rows_updated = queryset.update(question_status='p')
    if rows_updated == 1:
      message_bit = "1 questão foi publicada"
    else:
      message_bit = "%s questões foram publicadas" % rows_updated
    self.message_user(request, "%s com sucesso." % message_bit)
  publish_question.short_description = "Publicar questões"

  def unpublish_question(self, request, queryset):
    rows_updated = queryset.update(question_status='u')
    if rows_updated == 1:
      message_bit = "1 questão foi despublicada"
    else:
      message_bit = "%s questões foram despublicadas" % rows_updated
    self.message_user(request, "%s com sucesso." % message_bit)
  unpublish_question.short_description = "Despublicar questões"

  def publish_result(self, request, queryset):
    rows_updated = queryset.update(answer_status='p')
    if rows_updated == 1:
      message_bit = "1 questão"
    else:
      message_bit = "%s questões" % rows_updated
    self.message_user(request, "Os resultados de %s  foram publicados com sucesso." % message_bit)
  publish_result.short_description = "Publicar resultado das questões"

  def unpublish_result(self, request, queryset):
    rows_updated = queryset.update(answer_status='u')
    if rows_updated == 1:
      message_bit = "1 questão"
    else:
      message_bit = "%s questões" % rows_updated
    self.message_user(request, "Os resultados de %s foram despublicados com sucesso." % message_bit)
  unpublish_result.short_description = "Despublicar resultado das questões"


class UserProfileInline(admin.StackedInline):
  model = User
  can_delete = False
  verbose_name_plural = 'perfil'


# Define a new UserAdmin
class UserAdmin(UserAdmin):
  inlines = [UserProfileInline]


class AnswerAdmin(admin.ModelAdmin):
  actions = ['show_results']
  list_display = ['user', 'user_dept', 'question', '__str__']
  list_filter = ['question']

  def show_results(self, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return render(request, 'admin/resultados_admin.html', {'objects': queryset} )
  show_results.short_description = "Mostrar resultados"

# Remove default User page and activate the new version
admin.site.unregister(AuthUser)
admin.site.register(AuthUser, UserAdmin)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
