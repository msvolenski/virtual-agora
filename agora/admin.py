from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Choice, Question, User, Answer
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import date
from django.contrib.auth.models import User as AuthUser


############################################################

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

################################################################

class QuestionAdmin(admin.ModelAdmin):
  fields = ['question_text', 'image', ('question_type', 'days'), ('tags', 'question_status')]

  inlines = [ChoiceInline]

  list_filter = ('pub_date', 'exp_date', 'question_type')
  search_fields = ['question_text']
  list_display = ['question_text', 'id', 'pub_date', 'exp_date', 'question_type', 'is_question_published', 'is_answer_published','address']
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

#  def publish_result(self, request, queryset):
#    rows_updated = queryset.update(answer_status='p')
#    if rows_updated == 1:
#      message_bit = "1 questão"
#    else:
#      message_bit = "%s questões" % rows_updated
#    self.message_user(request, "Os resultados de %s  foram publicados com sucesso." % message_bit)
#  publish_result.short_description = "Publicar resultado das questões"
#
#  def unpublish_result(self, request, queryset):
#    rows_updated = queryset.update(answer_status='n')
#    if rows_updated == 1:
#      message_bit = "1 questão"
#    else:
#      message_bit = "%s questões" % rows_updated
#    self.message_user(request, "Os resultados de %s foram despublicados com sucesso." % message_bit)
#  unpublish_result.short_description = "Despublicar resultado das questões"

############################################################################################################
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
  model = User
  can_delete = False
  verbose_name_plural = 'profile'

############################################################################################################
# Define a new User admin
class UserAdmin(UserAdmin):
  inlines = [UserProfileInline]


###############################################################################################################3
class AnswerAdmin(admin.ModelAdmin):
  actions = ['show_results']
  list_display = ['user', 'user_dept', 'question', '__str__']
  list_filter = ['question', 'choice']

  def show_results(self, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return render(request, 'admin/resultados_admin.html', {'objects': queryset} )

##############################################################################################################





##RETIRAR

class VotoDoUsuarioAdmin(admin.ModelAdmin):    
    
    actions = ['mostrar_resultado']
    list_display = ('user', 'faculdade','questao' , 'voto' )
    list_filter = ('faculdade', 'questao')
    
    def mostrar_resultado(modeladmin, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return render(request, 'admin/resultados_admin.html', {'objects': queryset} )
#########################






admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.unregister(AuthUser)
admin.site.register(AuthUser, UserAdmin)



###RETIRAR
#admin.site.register(VotoDoUsuario, VotoDoUsuarioAdmin)