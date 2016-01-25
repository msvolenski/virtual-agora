from django.contrib import admin

from .models import Choice, Question, AdicionaLink, VotoDoUsuario, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render

def publicar_resultado(Question, request, queryset):
    queryset.update(resultado='p')
    queryset.update(permissao = 1)
 
def desfazer_publicacao_do_resultado(Question, request, queryset):
    queryset.update(resultado='n')
    queryset.update(permissao = 0)   

#==============================================================================
# Inclui no Admin a possibilidade de fazer as alternativas de cas Question
#==============================================================================
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


#==============================================================================
# Inclui no Admin uma página mostrando as Questions e uma página para fazer Questions
#==============================================================================
class QuestionAdmin(admin.ModelAdmin):
    
    list_filter = ['pub_date']    
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Tags', {'fields': ['tags']}),
        ('Tipo', {'fields': ['question_type']}),
        
    ]
    inlines = [ChoiceInline]
    
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'resultado')
    
    search_fields = ['question_text']
    actions = [publicar_resultado, desfazer_publicacao_do_resultado]
    
    class Media:
        js = (
            '/static/agora/admin/pageadmin.js',
        )
#==============================================================================
# Inclui no Admin uma página mostrando os link e uma página para incluir Links
#==============================================================================
class AdicionaLinknAdmin(admin.ModelAdmin):
    
    list_filter = ['data_publicacao']    
    
    #setam os campos que irão aparecer no "Add adiciona Link"    
    fieldsets = [
        (None,               {'fields': ['titulo']}),
        ('URL:', {'fields': ['url']}),         
        ('Data de publicação', {'fields': ['data_publicacao']}),
           
    ]
   
    
    list_display = ('titulo', 'url' , 'data_publicacao' )
    search_fields = ['titulo']

class VotoDoUsuarioAdmin(admin.ModelAdmin):    
    
    actions = ['mostrar_resultado']
    list_display = ('user', 'faculdade','questao' , 'voto' )
    list_filter = ('faculdade', 'questao')
    
    def mostrar_resultado(modeladmin, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return render(request, 'admin/resultados_admin.html', {'objects': queryset} )
    
   

# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )




#Coloca as classes em ação
admin.site.register(Question, QuestionAdmin)

admin.site.register(AdicionaLink, AdicionaLinknAdmin )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(VotoDoUsuario, VotoDoUsuarioAdmin)